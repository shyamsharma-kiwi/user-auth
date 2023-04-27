from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken

def send_otp(self, email, otp):
    subject = 'Your OTP'
    message = f'Your OTP is: {otp}'
    from_email = 'mohd.asad@kiwitech.com'
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list,
              auth_user="mohd.asad@kiwitech.com", auth_password="3339khanasad")


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh)
        ,
        'access': str(refresh.access_token),
    }
