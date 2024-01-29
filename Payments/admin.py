from django.contrib import admin
from .models import CharityPayments, InitiatedPayments

# Register your models here.
admin.site.register(CharityPayments)
admin.site.register(InitiatedPayments)