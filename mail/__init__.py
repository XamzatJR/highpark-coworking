from orm import User
import pathlib

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from setting import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings().email_username,
    MAIL_FROM=settings().email_from,
    MAIL_PASSWORD=settings().email_password,
    MAIL_PORT=465,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_SSL=True,
)

fm = FastMail(conf)


async def send_activation(url: str, user: User):
    with open(
        pathlib.Path(__file__).parent.joinpath("templates/verify.html"), encoding="utf8"
    ) as file:
        html = file.read().format(url + "auth/activate?code=" + user.code)
    message = MessageSchema(
        subject="Подтвердите свой аккаунт",
        recipients=[user.email],
        body=html,
        subtype="html",
    )
    await fm.send_message(message)
