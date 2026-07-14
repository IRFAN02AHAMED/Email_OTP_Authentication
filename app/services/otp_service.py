import os
import secrets
import smtplib
from datetime import datetime, timedelta, timezone
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()

FROM_EMAIL = os.getenv("EMAIL_ADDRESS")
APP_PASSWORD = os.getenv("EMAIL_APP_PASSWORD")


# Temporary OTP storage
# Later, replace this with PostgreSQL .
otp_storage: dict[str, dict] = {}


def generate_otp() -> str:
    """
    Generate a secure 6-digit OTP.
    """
    return f"{secrets.randbelow(1_000_000):06d}"



def send_otp_email(to_email: str, otp: str) -> None:
    """
    Send OTP through Gmail SMTP.
    """
    if not FROM_EMAIL or not APP_PASSWORD:
        raise ValueError(
            "EMAIL_ADDRESS or EMAIL_APP_PASSWORD is missing in the .env file."
        )

    message = EmailMessage()

    message["Subject"] = "OTP Verification"
    message["From"] = FROM_EMAIL
    message["To"] = to_email

    # Plain text fallback
    message.set_content(
        f"""
Hello,

Your OTP is: {otp}

This OTP is valid for 5 minutes.

Do not share this OTP with anyone.
"""
    )

    # HTML email
    message.add_alternative(
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
        subtype="html",
    )

    # Context manager automatically closes the SMTP connection
    with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as server:

        server.ehlo()  
        #EHLO basically a handshake
        #ehlo = extended hello
        #Hello, I am an SMTP client.
        # Tell me which features you support.

        server.starttls() #make the connection secure (TLS = Transport Layer Security)
        
        server.ehlo()
        # After TLS starts, the SMTP session is treated like a new secure session. 
        # Therefore, the client should send EHLO again to retrieve the features available after encryption.

        server.login(FROM_EMAIL, APP_PASSWORD)
        server.send_message(message)


def save_otp(email: str, otp: str) -> None:
    """
    Temporarily store OTP with a 5-minute expiry time.
    """
    otp_storage[email] = {
        "otp": otp,
        "expires_at": datetime.now(timezone.utc) + timedelta(minutes=5),
    }


"""
This function checks three things:

1. Is there an OTP stored for this email?
2. Has the OTP expired?
3. Does the entered OTP match?
"""

def verify_otp(email: str, entered_otp: str) -> bool:
    """
    Check whether the entered OTP is correct and not expired.
    """
    stored_data = otp_storage.get(email)

    if not stored_data:
        return False

    if datetime.now(timezone.utc) > stored_data["expires_at"]:
        otp_storage.pop(email, None)
        return False
    
    """
    timing attack - An attacker may send many guesses and measure how long each comparison takes.
    so we use secrets.compare_digest() to prevent timing attacks.

    It is designed to reduce timing differences caused by where the mismatch appears.

    It tries to examine the complete values rather than stopping at the first mismatching character.
    This makes it harder for an attacker to learn which characters matched.

    So we use this instead of == operator to compare the OTPs.
    
    """
    if not secrets.compare_digest(stored_data["otp"], entered_otp):
        return False

    # OTP can only be used once
    otp_storage.pop(email, None)

    return True

