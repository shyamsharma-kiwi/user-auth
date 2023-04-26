from django.urls import path, include
from account import views
from rest_framework.routers import DefaultRouter

from account.views import VerifyOTPView

router = DefaultRouter()

router.register(r'signup', views.SignUp, basename='signup'),

urlpatterns = [
    path('verify_otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('', include(router.urls))
]

