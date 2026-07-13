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
msg.set_content(
    f"""
Hello,

Your OTP is: {otp}

This OTP is valid for 5 minutes.

Do not share this OTP with anyone.
"""
)

msg.add_alternative(
    f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
</head>

<body style="
    margin: 0;
    padding: 0;
    background-color: #f4f6f8;
    font-family: Arial, sans-serif;
">

    <div style="
        max-width: 520px;
        margin: 40px auto;
        background-color: #ffffff;
        border-radius: 14px;
        padding: 32px;
        box-shadow: 0 4px 14px rgba(0,0,0,0.08);
        text-align: center;
    ">

        <h2 style="
            margin: 0 0 12px;
            color: #111827;
        ">
            Email Verification
        </h2>

        <p style="
            color: #4b5563;
            font-size: 16px;
            line-height: 1.6;
        ">
            Use the OTP below to verify your email address.
        </p>

        <div style="
            display: inline-block;
            margin: 24px 0;
            padding: 20px 32px;
            background-color: #f3f4f6;
            border: 2px solid #2563eb;
            border-radius: 12px;
            font-size: 36px;
            font-weight: bold;
            letter-spacing: 10px;
            color: #111827;
        ">
            {otp}
        </div>

        <p style="
            color: #4b5563;
            font-size: 15px;
        ">
            This OTP is valid for 5 minutes.
        </p>

        <p style="
            color: #9ca3af;
            font-size: 13px;
            margin-top: 24px;
        ">
            Do not share this OTP with anyone.
        </p>

    </div>

</body>
</html>
""",
    subtype="html"
)
# Send email
server.send_message(msg)

print("Email sent successfully!")

server.quit()