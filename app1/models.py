from django.db import models


from django.db import models
from django.contrib.auth.models import AbstractUser
import random

class CustomUser(AbstractUser):
    otp = models.CharField(max_length=6, blank=True, null=True)
    email_verified = models.BooleanField(default=False)

    def generate_otp(self):
        self.otp = str(random.randint(100000, 999999))
        self.save()
        return self.otp

    def __str__(self):
        return self.username  
class Calculation(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    num1 = models.FloatField()
    num2 = models.FloatField()
    operation = models.CharField(max_length=10)
    result = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.num1} {self.operation} {self.num2} = {self.result}"

