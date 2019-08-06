from django.db import models
from django.urls import reverse
from clients.models import Client
from django.contrib.auth.models import User

# Create your models here.
class Invoice(models.Model):
    class Meta:
        verbose_name = "invoice"
        verbose_name_plural = "invoices"

    def __str__(self):
        return  f"{str(self.date)}-{self.clientName}"

    def get_absolute_url(self):
        return reverse("invoice-list")
    
    @property
    def total(self):
        tot = 0
        for el in self.elements.all():
            tot += el.price
        return tot
    
    date = models.DateField(auto_now_add=True)
    clientName = models.CharField(max_length=100, blank=False, null=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='clients')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="invoices")

    def clean(self):
        super().clean()
        # from django.utils import timezone
        from django.core.validators import ValidationError

        if self.clientName == "Adam":
            raise ValidationError({"clientName": "Adam cannot  get an invoice!"})


    def save(self, *args, **kwargs):
        self.full_clean()
        # Pre-save
        super().save(*args, **kwargs)
        # Post-save

    @property
    def price_date(self):
        return "{} - {}".format(self.total, self.date)

class Element(models.Model):

    class Meta:
        verbose_name = "element"
        verbose_name_plural = "elements"

    def __str__(self):
        return self.name

    name = models.CharField(max_length=200, blank=False, null=False)
    price = models.IntegerField()
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name="elements")






# class Owner(models.Model):
# name = models.CharField(max_length=40)
# dog = models.ForeignKey(Dog, on_delete=models.CASCADE)

# def get_absolute_url(self):
#     return reverse("owners-single", kwargs={"id": self.id})
    
