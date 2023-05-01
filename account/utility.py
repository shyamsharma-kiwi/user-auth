import os
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken


def send_otp(self, email, otp):
    subject = 'Your OTP'
    message = f'Your OTP is: {otp}'
    from_email = os.environ.get('email_host_user')
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list,
              auth_user=os.environ.get('email_host_user'), auth_password=os.environ.get('EMAIL_HOST_PASSWORD'))


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh)
        ,
        'access': str(refresh.access_token),
    }
