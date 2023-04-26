from django.db import models

# Create your models here.


class UserRegister(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
