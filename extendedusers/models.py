from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

class ExtendedUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    taxCode = models.CharField(max_length=100)
    personal_picture = models.ImageField(upload_to="images/", blank=True)

    def __str__(self):
        return self.user.username