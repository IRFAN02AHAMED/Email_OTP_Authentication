# Commit Summary

## Commit 2 – Basic Email OTP Sending

### Features Implemented

- Configured Gmail SMTP using App Password.
- Loaded email credentials securely from the `.env` file.
- Generated a 6-digit OTP.
- Sent the OTP as a plain-text email.
- Successfully tested email delivery to the recipient.

---

## Commit 4 – HTML Styled OTP Email

### Features Implemented

- Added a professional HTML email template.
- Displayed the OTP inside a styled verification box.
- Improved the email layout using inline CSS.
- Included a plain-text fallback using `set_content()`.
- Added the HTML version using `add_alternative()` for better compatibility across email clients.

---

## Commit 5 – FastAPI Router & Service Architecture

### Features Implemented

- Converted the standalone script into a FastAPI application.
- Created a dedicated OTP router for API endpoints.
- Moved the OTP generation, email sending, and verification logic into a service layer.
- Added Pydantic schemas for request validation.
- Implemented temporary in-memory OTP storage.
- Added OTP expiration (5 minutes).
- Implemented OTP verification.
- Ensured OTPs are one-time-use by removing them after successful verification.
- Structured the project following a clean Router → Service architecture.

### Current Limitation

- OTPs are currently stored in an in-memory Python dictionary.
- The storage is temporary and intended only for development/testing.
- This will be replaced with PostgreSQL in a future update for persistent and scalable OTP management.
