from django.db import models
from django.urls import reverse

# Create your models here.
class Invoice(models.Model):
    class Meta:
        verbose_name = "invoice"
        verbose_name_plural = "invoices"

    def __str__(self):
        return  f"{str(self.date)}-{self.clientName}"

    def get_absolute_url(self):
        return reverse("invoice-list")
    
    # title = models.CharField(max_length=100, blank=False, null=False)
    date = models.DateField(auto_now_add=True)
    clientName = models.CharField(max_length=100, blank=False, null=False)
    totalPrice = models.IntegerField(blank=False)
    # clientAddress = models.CharField(max_length=100, blank=False, null=False)
    # clientCity = models.CharField(max_length=100, blank=False, null=False)
    # clientZip = models.CharField(max_length=100, blank=False, null=False)
    # clientCountry = models.CharField(max_length=100)
    # clientVat = models.CharField(max_length=100, blank=False, null=False)
    # tax = models.FloatField()
    # additionalNotes = models.TextField(max_length=100)

class Element(models.Model):

    class Meta:
        verbose_name = "element"
        verbose_name_plural = "elements"

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse("")
    name = models.CharField(max_length=200, blank=False, null=False)
    # quantity = models.IntegerField()
    price = models.IntegerField()
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)






# class Owner(models.Model):
# name = models.CharField(max_length=40)
# dog = models.ForeignKey(Dog, on_delete=models.CASCADE)

# def get_absolute_url(self):
#     return reverse("owners-single", kwargs={"id": self.id})
    
