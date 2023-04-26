from django.core.mail import send_mail


def send_otp(self, email, otp):
    subject = 'Your OTP'
    message = f'Your OTP is: {otp}'
    from_email = 'mohd.asad@kiwitech.com'
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list,
              auth_user="mohd.asad@kiwitech.com", auth_password="3339khanasad")
