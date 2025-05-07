import os
import json
import pytest
from datetime import datetime
from project import generate_prompt, book_appointment

# Test for generate_prompt
def test_generate_prompt():
    prompt = generate_prompt()
    assert isinstance(prompt, str)
    assert "appointment" in prompt
    assert "dental clinic" in prompt

# Fixture for cleaning up appointments file after test
@pytest.fixture
def clean_appointments_file():
    backup_file = None
    if os.path.exists("appointments.json"):
        with open("appointments.json", "r") as f:
            backup_file = f.read()
        os.remove("appointments.json")
    yield
    if backup_file is not None:
        with open("appointments.json", "w") as f:
            f.write(backup_file)

# Test for book_appointment
def test_book_appointment(clean_appointments_file):
    name = "Alice"
    date = "2025-12-31"
    time = "14:30"
    mobile = "+1234567890"
    
    book_appointment(name, date, time, mobile)

    with open("appointments.json", "r") as f:
        data = json.load(f)
    
    assert len(data) == 1
    assert data[0]["patient_name"] == name
    assert data[0]["date"] == date
    assert data[0]["time"] == time
    assert data[0]["mobile_no"] == mobile
