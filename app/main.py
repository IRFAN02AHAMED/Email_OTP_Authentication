from fastapi import FastAPI

from app.routers.otp_router import router as otp_router

app = FastAPI(
    title="Email OTP Authentication API",
    version="1.0.0",
)

app.include_router(otp_router)

