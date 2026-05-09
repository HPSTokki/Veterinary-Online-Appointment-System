from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
load_dotenv(os.path.join(BASE_DIR, ".env"))

def get_env(name: str) -> str:
    value = os.environ.get(name)
    if value is None:
        raise ValueError(f"Missing environment variable: {name}")
    return value

async def send_password_reset_email(
    to_email: str,
    pin: str
) -> None:
    body = f"""
    <h2>Password Reset Request</h2>
    <p>You requested to reset your password.</p>
    <p>Your PIN is:</p>
    <h1 style="letter-spacing: 8px; color: #2F5D4E; font-size: 36px;">{pin}</h1>
    <p>This PIN expires in <strong>10 minutes</strong>.</p>
    <p>If you did not request this, ignore this email.</p>
    <p>— Dr. Rosario Veterinary Clinic</p>
    """

    message = Mail(
        from_email=(get_env("MAIL_FROM"), "Dr. Rosario Veterinary Clinic"),
        to_emails=to_email,
        subject="Password Reset PIN — Dr. Rosario Vet Clinic",
        html_content=body
    )

    try:
        sg = SendGridAPIClient(get_env("SENDGRID_API_KEY"))
        sg.send(message)
    except Exception as e:
        print(f"Reset email failed: {e}")