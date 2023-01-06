import math
from random import random
from smtplib import SMTP, SMTPHeloError, SMTPAuthenticationError, SMTPNotSupportedError, SMTPException
from typing import Optional

from config import config
from exceptions import ValidationError


def new_otp() -> str:
    """
    Generate a new OTP.

    :return: OTP
    :rtype: str
    """

    otp = ""
    for i in range(6):
        otp += str(math.floor(random() * 10))

    return otp


def send_email(sender: str, recipients: list[str], message: str) -> bool:
    """
    Send and email.

    :param sender: Sender email
    :param recipients: List of emails
    :param message: Message content

    :return: True | False
    :rtype: bool
    """

    with SMTP("smtp.gmail.com", 587) as s:
        try:
            s.starttls()
            s.login(sender, config.app_password)
            s.sendmail(sender, recipients, message)
        except (SMTPHeloError, SMTPAuthenticationError, SMTPNotSupportedError, SMTPException) as e:
            raise e

    return True


def send_otp(sender: str, recipients: str, method: Optional[str] = "email") -> str:
    """
    Send OTP to email.

    :param sender: Email of sender
    :type sender: str
    :param recipients: List of emails
    :type recipients: list[str]
    :param method: Send method, defaults to ``email``
    :type method: Optional[str]

    :return: OTP code
    :rtype: str
    """

    otp = new_otp()
    if method == "email":
        send_email(sender=sender, recipients=[recipients], message=otp)

    return otp


if __name__ == '__main__':
    otp_code = send_otp(sender=config.sender, recipients=config.recipients)
    validate_otp = input("Enter OTP code: ")

    if not validate_otp == otp_code:
        raise ValidationError("Failed to validate OTP.")

    print("Super secret code validated.")
