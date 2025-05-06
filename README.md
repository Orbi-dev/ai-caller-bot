# ai-caller-bot
# AI Voice Appointment Bot 📞🤖

An open-source project to build an AI-powered voice appointment booking assistant using Twilio, Gemini AI, and Flask.

---

## 🚀 Features

- Real-time voice conversation with users
- Appointment booking using natural speech
- Saves appointment details securely
- Handles both speech input and backend processing
- Twilio-based call initiation and handling
- Gemini 2.0 Flash AI integration
- Easy to deploy, easy to extend

---

## 🛠️ Built With

- Python 3.10+
- Flask
- Twilio Voice API
- Gemini AI (Google GenAI)
- dotenv for environment configuration

---

## 📂 Project Structure

```plaintext
├── app.py            # Main Flask server
├── requirements.txt  # Python dependencies
├── .env.example      # Environment variable example
├── appointments.json # Appointment data storage
├── LICENSE
└── README.md
```

---

## ⚙️ Environment Variables

Create a `.env` file in the root:

```env
GEMINIAI_API_KEY=your-gemini-api-key
TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
FROM_PHONE_NUMBER=your-verified-twilio-number
NGROK_URL=https://your-ngrok-url.ngrok.io/voice
```

---

## 📞 API Endpoints

| Method | URL          | Description                  |
| ------ | ------------ | ---------------------------- |
| POST   | `/make_call` | Initiate a call to the user  |
| POST   | `/voice`     | Handle incoming voice call   |
| POST   | `/process`   | Handle user speech responses |

---

## 🧑‍💻 Local Development

```bash
git clone https://github.com/axixatechnologies/ai-voice-appointment-bot.git
cd ai-voice-appointment-bot
cp .env.example .env
pip install -r requirements.txt
python app.py
```

Expose using ngrok:

```bash
ngrok http 5000
```

Update `NGROK_URL` in `.env` file accordingly.

---

## 📝 License

This project is licensed under the [MIT License](LICENSE).

---

## ❤️ Contributing

Contributions are welcome!  
Please open an issue or submit a pull request to improve the project.

---

## 🌟 Star this Repo

If you like this project, please give it a ⭐️ on GitHub!
