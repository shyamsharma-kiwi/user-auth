from django.utils import timezone
from django.db import models
from django.contrib.auth.hashers import make_password

# Create your models here.


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

    def save(self, *args, **kwargs):
        """
            Function to hash password.
        """
        self.password = make_password(self.password)
        self.created_at = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        db_table = "account_userregister"
