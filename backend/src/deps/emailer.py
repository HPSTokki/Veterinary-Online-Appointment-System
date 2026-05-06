from fastapi_mail import MessageType, MessageSchema, FastMail, ConnectionConfig
from pydantic import SecretStr, NameEmail
import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
load_dotenv(os.path.join(BASE_DIR, ".env"))

def get_env(name: str) -> str:
    value = os.environ.get(name)
    if value is None:
        raise ValueError(f"Missing environment variable: {name}")
    return value

conf = ConnectionConfig(
    MAIL_USERNAME=get_env("MAIL_USERNAME"),
    MAIL_PASSWORD=SecretStr(get_env("MAIL_PASSWORD")),
    MAIL_FROM=get_env("MAIL_FROM"),
    MAIL_PORT=int(os.environ.get("MAIL_PORT", 587)),
    MAIL_SERVER=get_env("MAIL_SERVER"),
    MAIL_FROM_NAME="Dr. Rosario Veterinary Clinic",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True
)

fastmail = FastMail(conf)

async def send_password_reset_email(
    to_email: str,
    pin: str
) -> None:
    subject = "Password Reset PIN — Dr. Rosario Vet Clinic"
    body = f"""
    <h2>Password Reset Request</h2>
    <p>You requested to reset your password.</p>
    <p>Your PIN is:</p>
    <h1 style="letter-spacing: 8px; color: #2F5D4E; font-size: 36px;">{pin}</h1>
    <p>This PIN expires in <strong>10 minutes</strong>.</p>
    <p>If you did not request this, ignore this email.</p>
    <p>— Dr. Rosario Veterinary Clinic</p>
    """

    message = MessageSchema(
        subject=subject,
        recipients=[NameEmail(name="", email=to_email)],
        body=body,
        subtype=MessageType.html
    )

    try:
        await fastmail.send_message(message)
    except Exception as e:
        print(f"Reset email failed: {e}")