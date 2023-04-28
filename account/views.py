import random
from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import serializers

from account.messages import ERROR_CODE, SUCCESS_CODE
from account.models import UserRegister
from account.serializers import UserSignUpSerializer, VerifyOTPSerializer, UserLoginSerializer, LogInVerifyOTPSerializer
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.hashers import check_password
from account.utility import send_otp, get_tokens_for_user


class SignUp(GenericViewSet, CreateModelMixin):
    """View to register user"""
    queryset = User.objects.all()
    serializer_class = UserSignUpSerializer
    permission_classes = [AllowAny, ]
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(serializer.validated_data)
            return Response({"message": "User created successfully. Please check your registered email for "
                                        "OTP to activate your account."},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'OTP verified successfully and account activated!'
                             }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericViewSet, CreateModelMixin):
    """
    This Api is used for send OTP to verify the user and take email and password to verify.
    """
    serializer_class = UserLoginSerializer
    queryset = UserRegister.objects.all()

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL,
                                        example='user@example.com'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD,
                                           example='password'),
            },
            required=['email', 'password']
        ),
        responses={
            200: 'OTP generated successfully',
            400: 'Invalid request body',
            401: 'Invalid credentials'
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = request.data["email"]
            password = request.data["password"]
            number = random.randint(100000, 999999)
            user = UserRegister.objects.get(email=email)
            if user.is_active:
                if check_password(password, user.password):
                    user.otp = number
                    user.save()
                    send_otp(self, email, number)
                    return Response({"detail": SUCCESS_CODE['2000']})
            else:
                raise serializers.ValidationError({"detail": ERROR_CODE['4003']})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyUserOTPView(GenericViewSet, CreateModelMixin):
    """
    This Api is to verify the user by OTP send on email
   """
    serializer_class = LogInVerifyOTPSerializer
    queryset = UserRegister.objects.all()

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL,
                                        example='user@example.com'),
                'otp': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    minLength=6,
                    maxLength=6,
                    example='123456',
                    description='A 6-digit OTP sent to the user',
                )
            },
            required=['email', 'OTP']
        ),
        responses={
            200: 'OTP verify successfully',
            400: 'Invalid request body',
            401: 'Invalid credentials'
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = LogInVerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = UserRegister.objects.get(email=request.data.get('email'), otp=request.data.get('otp'))
            token = get_tokens_for_user(user)
            return Response({'token': token, 'message': 'OTP verified successfully and account activated!'
                             }, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
