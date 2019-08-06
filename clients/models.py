from django.db import models
from django.urls import reverse
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
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    taxCode = models.CharField(max_length=100)

