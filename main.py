import requests
import hashlib
from datetime import date, timedelta
import email_client
import os
from dotenv import load_dotenv

def authenticate():
    NONCE_URL = os.getenv('NONCE_URL')
    LOGIN_URL = os.getenv('LOGIN_URL')

    session = requests.Session()

    nonce_response = session.post(NONCE_URL)
    nonce_data = nonce_response.json()
    nonce1 = nonce_data.get("nonce1")
    nonce2 = nonce_data.get("nonce2")

    password = os.getenv('PASSWORD')
    username = os.getenv('USERNAME')

    payload = {
        'nonce1': nonce1,
        'nonce2': nonce2,
        'pass': md5_hash(nonce2 + username + password),
        'user': md5_hash(nonce1 + username)
    }
    response = session.post(LOGIN_URL, json=payload, headers=generate_headers())
    return session

def book_laundry(session):
    BOOKING_URL = os.getenv('BOOKING_URL')

    target = date.today() + timedelta(days=7)
    _, iso_week, _ = target.isocalendar()

    booking_payload = {
        'Date': target.strftime('%Y-%m-%d'),
        'ObjectId': 19,
        'SchedulePeriodId': 4,
        'weekNumber': iso_week
    }

    response_booking = session.post(BOOKING_URL, json=booking_payload, headers=generate_headers())

    if response_booking.status_code != 200:
        email_client.send_email("Tvättstugan", "Systemfel!")
    for booking in response_booking.json()['Bookings']:
        if booking['WeekNumber'] == iso_week and booking['SchedulePeriodId'] == 4:
            if booking['IsOwned'] != True:
                email_client.send_email("Tvättstugan", "Hallå där! Någon jäkel har snott din tvättid!")
                break
            else:
                print("Laundry booked successfully!")
                break

def generate_headers():
    return {
        "Content-Type": "application/json;charset=UTF-8",
        "User-Agent": "Mozilla/5.0",
        "X-Requested-With": "XMLHttpRequest"
    }

def md5_hash(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

if __name__ == "__main__":
    load_dotenv()
    session = authenticate()
    book_laundry(session)
