from rest_framework import routers
from account.views import LoginView, VerifyUserOTPView, VerifyOTPView
from django.urls import path
from account import views


router = routers.DefaultRouter()
router.register('login', LoginView, basename='user-login')
router.register('verify_login_otp', VerifyUserOTPView, basename='user-otp-verify')
router.register(r'signup', views.SignUp, basename='signup'),

urlpatterns = [
    path('verify_otp/', VerifyOTPView.as_view(), name='verify_otp'),
]+router.urls

