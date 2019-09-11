from django.contrib import admin
from .models import ExtendedUser, VerificationTokens
# Register your models here.

admin.site.register(ExtendedUser)

@admin.register(VerificationTokens)
class VFTAdmin(admin.ModelAdmin):
    list_display = ('account', 'token', )
