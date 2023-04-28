import os

from django.core.mail import send_mail


def send_otp(self, email, otp):
    subject = 'Your OTP'
    message = f'Your OTP is: {otp}'
    from_email = 'mohd.asad@kiwitech.com'
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list,
              auth_user=os.environ.get('auth_user'), auth_password=os.environ.get('auth_password'))
