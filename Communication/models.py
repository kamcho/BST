from django.db import models

from Users.models import MyUser

# Create your models here.
class MessagingSettings(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    sms = models.BooleanField(default=False)
    whatsapp = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)