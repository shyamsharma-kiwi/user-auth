from rest_framework import status
from drf_yasg import openapi

from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny

from django.contrib.auth.models import User
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from account.messages import VIEWS_MESSAGES
from account.models import UserRegister
from account.serializers import UserSignUpSerializer, VerifyOTPSerializer
from drf_yasg.utils import swagger_auto_schema


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
                'otp': openapi.Schema(type=openapi.TYPE_STRING),
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
            return Response({'message': VIEWS_MESSAGES['otp_verification']['verified']
                             }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
