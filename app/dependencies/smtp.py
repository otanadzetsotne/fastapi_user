from smtplib import SMTP

from fastapi import Depends

from .settings import get_settings, Settings


def get_smtp(
        settings: Settings = Depends(get_settings),
) -> SMTP:
    """
    Yield SMTP connection and then close it
    """

    smtp = SMTP(
        host=settings.smtp.host,
        port=settings.smtp.port,
    )

    try:
        yield smtp
    finally:
        smtp.quit()
