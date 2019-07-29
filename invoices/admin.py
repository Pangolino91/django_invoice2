from django.contrib import admin
from .models import Invoice, Element

# Register your models here.

admin.site.register(Invoice)
admin.site.register(Element)