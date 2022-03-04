from smtplib import SMTP
from pydantic import EmailStr


def send(
        smtp: SMTP,
        msg_to: EmailStr,
        msg: str,
):
    # TODO: Normal mailing
    # smtp.sendmail(settings.smtp.msg_from, msg_to, msg)
    pass
