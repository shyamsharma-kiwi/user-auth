from django.urls import path, include
from account import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r'signup', views.SignUp, basename='signup'),
router.register(r'verify_otp', views.VerifyOTPView, basename='verify_otp'),

urlpatterns = [
    path('', include(router.urls))
]

