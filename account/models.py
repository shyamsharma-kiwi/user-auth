from django.db import models
from django.contrib.auth.hashers import check_password as django_check_password


class UserRegister(models.Model):
    """
        Model to store User Registration Details.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True)

    def check_password(self, raw_password):
        return django_check_password(raw_password, self.password)
