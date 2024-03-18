from django.contrib import admin
from .models import MessagingSettings, Inbox
# Register your models here.
admin.site.register(MessagingSettings)
admin.site.register(Inbox)
