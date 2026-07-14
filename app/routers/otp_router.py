from fastapi import APIRouter, HTTPException, status

from app.schemas.otp_schema import SendOTPRequest, VerifyOTPRequest
from app.services.otp_service import (
    generate_otp,
    save_otp,
    send_otp_email,
    verify_otp,
)
import smtplib

router = APIRouter(
    prefix="/auth/otp",
    tags=["OTP Authentication"],
)


@router.post("/send")
def send_otp(request: SendOTPRequest):
    """
    Generate and send an OTP to the given email address.
    """
    try:
        otp = generate_otp()

        send_otp_email(
            to_email=request.email,
            otp=otp,
        )

        save_otp(
            email=request.email,
            otp=otp,
        )

        return {
            "success": True,
            "message": "OTP sent successfully.",
        }

    except smtplib.SMTPAuthenticationError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Gmail authentication failed. Check the email app password.",
        )

    except smtplib.SMTPException as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unable to send email: {str(error)}",
        )

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(error),
        )


@router.post("/verify")
def check_otp(request: VerifyOTPRequest):
    """
    Verify the OTP entered by the user.
    """
    is_valid = verify_otp(
        email=request.email,
        entered_otp=request.otp,
    )

    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP.",
        )

    return {
        "success": True,
        "message": "OTP verified successfully.",
    }