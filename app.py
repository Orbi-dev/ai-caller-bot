from flask import Flask, Response, request, jsonify
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.rest import Client
from google import genai
from google.genai import types
from datetime import datetime
from dotenv import load_dotenv
import os
import json

load_dotenv()
app = Flask(__name__)
client = genai.Client(api_key=os.getenv("GEMINIAI_API_KEY"))
APPOINTMENTS_FILE = "appointments.json"
active_chats = {}
VOICE_PARAMS = {
    "voice": "Polly.Aditi",
    "language": "en-IN",
}
twilio_client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))


def get_ai_reply(call_sid, user_input):
    chat = active_chats.get(call_sid)
    return chat.send_message(user_input) if chat else None


def generate_prompt():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return f"""
        You are an appointment scheduler for a dental clinic. Your job is to assist users in booking appointments with the doctor.
        If the user wants to book an appointment, politely ask for their name and the preferred date and time.
        If user says today, tomorrow, or after 1 hour, convert it based on current time: {now}
        If the user says anything unrelated to booking an appointment, gently remind them you only help with appointment-related queries.
    """


def book_appointment(patient_name, date, time, mobile_no):
    if not os.path.exists(APPOINTMENTS_FILE):
        with open(APPOINTMENTS_FILE, "w") as f:
            json.dump([], f)
    with open(APPOINTMENTS_FILE, "r+") as f:
        appointments = json.load(f)
        appointments.append(
            {
                "patient_name": patient_name,
                "date": date,
                "time": time,
                "mobile_no": mobile_no,
            }
        )
        f.seek(0)
        json.dump(appointments, f, indent=4)


book_appointment_function = {
    "name": "bookAppointment",
    "description": "Books an appointment at a dental clinic.",
    "parameters": {
        "type": "object",
        "properties": {
            "patient_name": {"type": "string", "description": "The customer's name."},
            "date": {"type": "string", "description": "YYYY-MM-DD"},
            "time": {"type": "string", "description": "HH:MM"},
        },
        "required": ["patient_name", "date", "time"],
    },
}


@app.route("/voice", methods=["POST"])
def voice():
    response = VoiceResponse()

    call_sid = request.values.get("CallSid")
    if not call_sid:
        response.say("Sorry, something went wrong. Please try again.", **VOICE_PARAMS)
        return Response(str(response), mimetype="text/xml")

    if call_sid not in active_chats:
        chat = client.chats.create(
            model="gemini-2.0-flash",
            config=types.GenerateContentConfig(
                system_instruction=generate_prompt(),
                tools=[types.Tool(function_declarations=[book_appointment_function])],
            ),
        )
        active_chats[call_sid] = chat

    gather = Gather(input="speech", action="/process", method="POST", timeout=5)
    gather.say("Hello! How can I help you?", **VOICE_PARAMS)
    response.append(gather)
    return Response(str(response), mimetype="text/xml")


@app.route("/process", methods=["POST"])
def process():
    call_sid = request.values.get("CallSid")
    user_phone = request.values.get("From")
    user_input = request.values.get("SpeechResult", "Ask user to speak louder.")
    ai_response = get_ai_reply(call_sid, user_input)
    response = VoiceResponse()

    if not ai_response:
        response.say("Sorry, something went wrong. Please try again.", **VOICE_PARAMS)
        return Response(str(response), mimetype="text/xml")

    part = ai_response.candidates[0].content.parts[0]
    if hasattr(part, "function_call") and part.function_call:
        func = part.function_call
        new_data = {**func.args, "mobile_no": user_phone}
        book_appointment(**new_data)
        del active_chats[call_sid]
        response.say("Thanks, we are waiting for you on time.", **VOICE_PARAMS)
    else:
        reply = part.text.strip()
        gather = Gather(input="speech", action="/process", method="POST", timeout=5)
        gather.say(reply, **VOICE_PARAMS)
        response.append(gather)

    return Response(str(response), mimetype="text/xml")


@app.route("/make_call", methods=["POST"])
def make_call():
    to_phone_no = request.values.get("to_phone_no")

    call = twilio_client.calls.create(
        to=to_phone_no,
        from_=os.getenv("FROM_PHONE_NUMBER"),
        url=os.getenv("NGROK_URL"),
    )

    return (
        jsonify(
            {"status": "success", "message": "Call initiated", "call_sid": call.sid}
        ),
        200,
    )


@app.route("/")
def index():
    return "✅ Twilio + Gemini AI Voice Bot Running"


if __name__ == "__main__":
    app.run(debug=True, port=5000)
