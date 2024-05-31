import os
import sys

from dotenv import load_dotenv
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
import logging
import ssl

from fastapi import FastAPI, BackgroundTasks
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage



logger = logging.getLogger("uvicorn")
ssl._create_default_https_context = ssl._create_unverified_context

load_dotenv()
SENDER_GMAIL = 'im.asif093@gmail.com'
SENDER_GMAIL_PASSWORD = 'zjvi pexj nrku vslu'
dirname = os.path.dirname(__file__)
templates_folder = os.path.join(dirname, '../templates')

conf = ConnectionConfig(
    MAIL_USERNAME=SENDER_GMAIL,
    MAIL_PASSWORD=SENDER_GMAIL_PASSWORD,
    MAIL_FROM=SENDER_GMAIL,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="FastAPI forgot password example",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=False,
    TEMPLATE_FOLDER=templates_folder,
)


async def send_registration_notification(password, recipient_email):
    template_body = {
        "email": recipient_email,
        "password": password
    }

    try:
        message = MessageSchema(
            subject="FastAPI forgot password application registration",
            recipients=[recipient_email],
            template_body=template_body,
            subtype=MessageType.html
        )
        fm = FastMail(conf)
        await fm.send_message(message, template_name="registration_notification.html")
    except Exception as e:
        logger.error(f"Something went wrong in registration email notification")
        logger.error(str(e))


async def send_reset_password_mail(recipient_email, user, url, expire_in_minutes):
    template_body = {
        "user": user,
        "url": url,
        "expire_in_minutes": expire_in_minutes
    }
    try:
        message = MessageSchema(
            subject="FastAPI forgot password application reset password",
            recipients=[recipient_email],
            template_body=template_body,
            subtype=MessageType.html
        )
        fm = FastMail(conf)
        await fm.send_message(message, template_name="reset_password_email.html")
    except Exception as e:
        msg = "Error [{0}] at line [{1}]".format(str(e), sys.exc_info()[2].tb_lineno)
        logger.error(f'From send_reset_password_mail  {msg}', exc_info=e)


def send_email_with_images_and_count(email_to: str, subject: str, message: str, image_paths: list, pallets_count: int):
    msg = MIMEMultipart()
    msg['From'] = SENDER_GMAIL
    msg['To'] = email_to
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    # Attach images
    for img_path in image_paths:
        with open(img_path, 'rb') as img_file:
            img_data = img_file.read()
            image = MIMEImage(img_data, name='image.png')
            msg.attach(image)

    # Add pallets count to message
    msg.attach(MIMEText(f"Pallets Count: {pallets_count}", 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(SENDER_GMAIL, SENDER_GMAIL_PASSWORD)
            smtp.send_message(msg)
    except Exception as e:
        print("Failed to send email:", str(e))


