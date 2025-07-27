import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

def send_email():
    load_dotenv()
    password = os.getenv('APP_PASSWORD')
    sender_email = os.getenv('EMAIL')
    receiver_email = os.getenv('EMAIL')
    subject = "Tvättstugan"
    body = "Hallå där! Någon jäkel har snott din tvättid!"

    msg = EmailMessage()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, password)
            smtp.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    send_email()