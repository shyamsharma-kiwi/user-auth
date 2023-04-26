from rest_framework import routers
from django.urls import path
from account.views import LoginView, VerifyUserOTPView

router = routers.DefaultRouter()
router.register('login', LoginView, basename='user-login')
router.register('verify_login_otp', VerifyUserOTPView, basename='user-otp-verify')

urlpatterns = [
    # path('verify_login_otp/', VerifyUserOTPView.as_view(), name='verify_otp'),
]+router.urls
