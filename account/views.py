import random
from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import serializers

from account.constants import *
from account.messages import VIEWS_MESSAGES
from account.messages import ERROR_CODE, SUCCESS_CODE
from account.models import UserRegister
from account.serializers import UserSignUpSerializer, VerifyOTPSerializer, UserLoginSerializer, LogInVerifyOTPSerializer
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

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD),
                'confirm_password': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_PASSWORD),
            }
        ),
        responses={
            201: VIEWS_MESSAGES['signup']['success'],
            400: VIEWS_MESSAGES['signup']['invalid'],
            401: VIEWS_MESSAGES['signup']['unauthorized']
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            user = serializer.create(serializer.validated_data)
            return Response({"message": VIEWS_MESSAGES['signup']['success']},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(GenericViewSet, CreateModelMixin):
    """
    This Api is to verify the OTP send on email
   """
    serializer_class = VerifyOTPSerializer
    queryset = UserRegister.objects.all()

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_EMAIL,
                                        example='user@example.com'),
                'otp': openapi.Schema(type=openapi.TYPE_STRING,
                                      minLength=max_length_otp,
                                      maxLength=max_length_otp,
                                      example='123456'),
            }
        ),
        responses={
            200: VIEWS_MESSAGES['otp_verification']['verified'],
            400: VIEWS_MESSAGES['otp_verification']['invalid'],
            401: VIEWS_MESSAGES['otp_verification']['unauthorized']
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = UserRegister.objects.get(email=request.data.get('email'), otp=request.data.get('otp'))

            return Response({'message': VIEWS_MESSAGES['otp_verification']['verified']
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
