from django.core.mail import EmailMessage


def send_email(subject: str, message: str, mail_to: str) -> None:
    email = EmailMessage(subject, message, to=[mail_to],from_email="aparking.g11@gmail.com", )
    response = email.send()
    return response

