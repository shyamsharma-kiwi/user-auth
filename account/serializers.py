from rest_framework import serializers
from account.models import UserRegister


class UserLoginSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)



class LogInVerifyOTPSerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)
    email = serializers.EmailField(required=True)

    def validate_otp(self, value):
        otp_obj = UserRegister.objects.filter(otp=value).first()
        if not otp_obj:
            raise serializers.ValidationError('Invalid OTP')
        return value

    def create(self, validated_data):
        otp = validated_data.get('otp')
        otp_obj = UserRegister.objects.filter(otp=otp).first()
        otp_obj.is_active = True
        otp_obj.save()
        return validated_data
