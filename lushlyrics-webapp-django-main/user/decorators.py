from django.conf import settings
from django.core.mail import send_mail


def send_forget_password_mail(email, token):
    id = email.id
    subject = 'Forgot Password Youtify'
    message = f'Click this link to reset your password! \n http://127.0.0.1:8000/change-password/{id}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email.email]
    send_mail(subject, message, email_from, recipient_list)
    return True
