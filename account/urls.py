from rest_framework import routers
from account.views import LoginView, VerifyUserOTPView
from django.urls import path, include
from account import views


router = routers.DefaultRouter()
router.register('login', LoginView, basename='user-login')
router.register('verify_login_otp', VerifyUserOTPView, basename='user-otp-verify')
router.register(r'signup', views.SignUp, basename='signup'),
router.register(r'verify_otp', views.VerifyOTPView, basename='verify_otp'),

urlpatterns = [
    path('', include(router.urls)),
]


