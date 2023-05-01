import sys

from account.constants import MODEL_CONSTANT
from account.messages import ERROR_CODE
from account.models import UserRegister
from account.utility import send_otp
from django.contrib.auth.hashers import make_password

sys.path.append("..")
from datetime import timezone
from random import random
from rest_framework import serializers
import re
import sys

sys.path.append("..")
import random
from django.utils import timezone


class UserSignUpSerializer(serializers.ModelSerializer):
    """Serializer to Register user"""
    first_name = serializers.CharField(max_length=20, min_length=2, required=True,
                                       trim_whitespace=False)
    last_name = serializers.CharField(max_length=20, min_length=2, required=True,
                                      trim_whitespace=False)
    email = serializers.EmailField(required=True)

    password = serializers.CharField(max_length=20, min_length=8, required=True,
                                     write_only=True, trim_whitespace=False)
    confirm_password = serializers.CharField(max_length=20, min_length=8, required=True,
                                             write_only=True)

    class Meta:
        model = UserRegister
        fields = ('id', 'password', 'confirm_password', 'first_name', 'last_name', 'email')

    def validate_password(self, value, user=None):
        regex = re.compile(r'^(?=.*[!@#$%^&*()_+\-=[\]{};:\'"\\|,.<>/?])(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[^\s]{8,}$')
        if not regex.match(value):
            raise serializers.ValidationError("Password must contain at least one special character, one capital "
                                              "letter, one small letter, and one number, with a length of at least 8 "
                                              "and no spaces.")
        return value

    def validate_first_name(self, value):
        """
            Field level validation to validate first name
        """
        if not any(char.isalpha() for char in value):
            raise serializers.ValidationError("First Name should contain at least one alphabet.")
        if not value.isalpha() or ' ' in value:
            raise serializers.ValidationError("Invalid First name. Only Alphabets are allowed.")
        return value

    def validate_last_name(self, value):
        """
            Field level validation to validate last name
        """
        if not any(char.isalpha() for char in value):
            raise serializers.ValidationError("Last Name should contain at least one alphabet.")
        if not value.isalpha() or ' ' in value:
            raise serializers.ValidationError("Invalid last name. Only Alphabets are allowed.")
        return value

    def validate(self, data):
        """
            Object level validation to check weather the given field exist or not and to match passwords
        """
        email = data.get('email')
        password = data.get('password')
        c_password = data.get('confirm_password')

        if UserRegister.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists!")
        if password != c_password:
            raise serializers.ValidationError("Password and confirm password does not match!")
        return data

    def create(self, validated_data):
        email = validated_data.get('email')
        otp = str(random.randint(100000, 999999))
        """
            create function to create validated user data
        """
        user = UserRegister.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=make_password(validated_data['password']),
            otp=otp,
        )

        send_otp(self, email, otp)
        return user


class VerifyOTPSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)

    def validate_otp(self, value):
        otp_obj = UserRegister.objects.filter(otp=value).first()
        if not otp_obj:
            raise serializers.ValidationError('Invalid OTP')
        elif (timezone.now() - otp_obj.created_at).seconds > 300:
            raise serializers.ValidationError('OTP expired')
        return value

    def create(self, validated_data):
        otp = validated_data.get('otp')
        otp_obj = UserRegister.objects.filter(otp=otp).first()
        otp_obj.is_active = True
        otp_obj.save()
        return validated_data


class UserLoginSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    def validate(self, data):
        # Validate email
        email = data.get('email')
        if not email:
            raise serializers.ValidationError({"detail": ERROR_CODE['4004']})
        if not UserRegister.objects.filter(email=email).exists():
            raise serializers.ValidationError({"detail": ERROR_CODE['4005']})

        # Validate password
        password = data.get('password')
        if not password:
            raise serializers.ValidationError({"detail": ERROR_CODE['4006']})
        user = UserRegister.objects.get(email=email)
        if not user.check_password(password) and user.is_active == True:
            raise serializers.ValidationError({"detail": ERROR_CODE['4007']})
        return data


class LogInVerifyOTPSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=MODEL_CONSTANT['max_length_otp'])
    email = serializers.EmailField(required=True)

    def validate(self, data):
        try:
            user_obj = UserRegister.objects.get(email=data.get('email'))
            if user_obj.otp != data.get('otp'):
                raise serializers.ValidationError({"detail": ERROR_CODE['4001']})
        except UserRegister.DoesNotExist:
            raise serializers.ValidationError({"detail": ERROR_CODE['4002']})
        return data

    def create(self, validated_data):
        otp = validated_data.get('otp')
        email = validated_data.get('email')
        otp_obj = UserRegister.objects.filter(email=email, otp=otp).first()
        user = UserRegister.objects.get(email=email)
        if user.is_active:
            if otp_obj:
                otp_obj.is_active = True
                otp_obj.save()
        else:
            raise serializers.ValidationError({"detail": ERROR_CODE['4003']})
        return validated_data
