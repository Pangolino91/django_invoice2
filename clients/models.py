from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.


class Client(models.Model):
    class Meta:
        verbose_name = "client"
        verbose_name_plural = "clients"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("-detail", kwargs={"pk": self.pk})

    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    companyName = models.CharField(max_length=150, blank=True)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    taxCode = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="clients", default="")

