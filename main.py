import os
import random
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv

# Load .env
load_dotenv()

FROM_EMAIL = os.getenv("EMAIL_ADDRESS")
APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")

# Generate 6-digit OTP
otp = ""

for _ in range(6):
    otp += str(random.randint(0, 9))

print("Generated OTP:", otp)

# Connect to Gmail SMTP
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()

# Login
server.login(FROM_EMAIL, APP_PASSWORD)

# Recipient email
to_mail = input("Enter recipient email: ")

# Create email
msg = EmailMessage()

msg["Subject"] = "OTP Verification"
msg["From"] = FROM_EMAIL
msg["To"] = to_mail

msg.set_content(f"""
Hello,

Your OTP is: {otp}

This OTP is valid for 5 minutes.

Do not share this OTP with anyone.

Regards,
OTP Verification System
""")

# Send email
server.send_message(msg)

print("Email sent successfully!")

server.quit()