import random
from rest_framework import serializers
from account.models import UserRegister
from account.serializers import UserLoginSerializer, LogInVerifyOTPSerializer
from account.utility import send_otp, get_tokens_for_user
from rest_framework import status
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from account.serializers import UserSignUpSerializer
from rest_framework.views import APIView

class LoginView(GenericViewSet, CreateModelMixin):
    """
    This Api is used for send OTP to verify the user and take email and password to verify.
    """
    serializer_class = UserLoginSerializer
    queryset = UserRegister.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = request.data["email"]
            password = request.data["password"]
            if email is None:
                raise serializers.ValidationError('An email address is required to log in.')

            if password is None:
                raise serializers.ValidationError('A password is required to log in.')

            number = random.randint(100000, 999999)
            user = UserRegister.objects.get(email=email, password=password)
            user.otp = number
            user.save()
            print(number)
            send_otp(self, email, number)
            return Response("otp generated success")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyUserOTPView(GenericViewSet, CreateModelMixin):
    """
    This Api is to verify the user by OTP send on email
   """
    serializer_class = LogInVerifyOTPSerializer
    queryset = UserRegister.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = LogInVerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = UserRegister.objects.get(email=request.data.get('email'), otp=request.data.get('otp'))
            token = get_tokens_for_user(user)
            return Response({'token': token, 'message': 'OTP verified successfully and account activated!'
                             }, status=status.HTTP_200_OK)


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
            return Response({"message": "User created successfully"},
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
