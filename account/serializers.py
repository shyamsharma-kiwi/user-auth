import sys
from account.constants import *
from account.messages import SIGNUP_VALIDATION_ERROR, OTP_VALIDATION_ERROR
from account.messages import ERROR_CODE
from account.models import UserRegister
from account.utility import send_otp
from random import random
from rest_framework import serializers
import re
from django.contrib.auth.hashers import make_password
import random
sys.path.append("..")


class UserSignUpSerializer(serializers.ModelSerializer):
    """Serializer to Register user"""
    first_name = serializers.CharField(max_length=max_length, min_length=min_length, required=required,
                                       trim_whitespace=trim_whitespace)
    last_name = serializers.CharField(max_length=max_length, min_length=min_length, required=required,
                                      trim_whitespace=trim_whitespace)
    email = serializers.EmailField(required=required)

    password = serializers.CharField(max_length=max_length, min_length=min_length_pass, required=required,
                                     write_only=required, trim_whitespace=trim_whitespace)
    confirm_password = serializers.CharField(max_length=max_length, min_length=min_length_pass, required=required,
                                             write_only=required)

    class Meta:
        model = UserRegister
        fields = ('id', 'password', 'confirm_password', 'first_name', 'last_name', 'email')

    def validate_password(self, value, user=None):
        """
            Field level validation to validate Password
        """
        regex = re.compile(r'^(?=.*[!@#$%^&*()_+\-=[\]{};:\'"\\|,.<>/?])(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[^\s]{8,}$')
        if not regex.match(value):
            raise serializers.ValidationError(SIGNUP_VALIDATION_ERROR['password']['invalid'])
        return value

    def validate_first_name(self, value):
        """
            Field level validation to validate first name
        """
        if not any(char.isalpha() for char in value):
            raise serializers.ValidationError(SIGNUP_VALIDATION_ERROR['first_name']['invalid'])
        if not value.isalpha() or ' ' in value:
            raise serializers.ValidationError(SIGNUP_VALIDATION_ERROR['first_name']['required'])
        return value

    def validate_last_name(self, value):
        """
            Field level validation to validate last name
        """
        if not any(char.isalpha() for char in value):
            raise serializers.ValidationError(SIGNUP_VALIDATION_ERROR['last_name']['invalid'])
        if not value.isalpha() or ' ' in value:
            raise serializers.ValidationError(SIGNUP_VALIDATION_ERROR['last_name']['required'])
        return value

    def validate(self, data):
        """
            Object level validation to check weather the given field exist or not and to match passwords
        """
        email = data.get('email')
        password = data.get('password')
        c_password = data.get('confirm_password')

        if UserRegister.objects.filter(email=email).exists():
            raise serializers.ValidationError(SIGNUP_VALIDATION_ERROR['email']['exits'])
        if password != c_password:
            raise serializers.ValidationError(SIGNUP_VALIDATION_ERROR['confirm_password']['invalid'])
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
    otp = serializers.CharField(max_length=max_length_otp)
    email = serializers.EmailField(required=True)
    """Serializer to Verify The OTP"""

    def validate(self, data):
        """
            Field level validation to validate OTP
        """
        try:
            user_obj = UserRegister.objects.get(email=data.get('email'))
            if user_obj.otp != data.get('otp'):
                raise serializers.ValidationError(OTP_VALIDATION_ERROR['invalid'])
        except UserRegister.DoesNotExist:
            raise serializers.ValidationError(OTP_VALIDATION_ERROR['expired'])
        return data

    def create(self, validated_data):
        """
            create function to set is_active true of user
        """
        otp = validated_data.get('otp')
        email = validated_data.get('email')
        otp_obj = UserRegister.objects.filter(email=email, otp=otp).first()
        if otp_obj:
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
        return validated_data
