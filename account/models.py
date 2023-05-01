from django.db import models
from django.contrib.auth.hashers import check_password as django_check_password

from account.constants import MODEL_CONSTANT


class UserRegister(models.Model):
    """
        Model to store User Registration Details.
    """
    first_name = models.CharField(max_length=MODEL_CONSTANT['max_length'])
    last_name = models.CharField(max_length=MODEL_CONSTANT['max_length'], null=True, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=MODEL_CONSTANT['max_length'])
    is_active = models.BooleanField(default=False)
    otp = models.CharField(max_length=MODEL_CONSTANT['max_length_otp'], null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)

    def check_password(self, raw_password):
        return django_check_password(raw_password, self.password)
