from django.db import models

from Users.models import MyUser

# Create your models here.
class MessagingSettings(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    sms = models.BooleanField(default=False)
    whatsapp = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)
    
class Inbox(models.Model):
    user = models.ForeignKey(MyUser, null=True, on_delete=models.CASCADE)
    names = models.CharField(max_length=60)
    phone = models.CharField(max_length=15, null=True)
    about = models.CharField(max_length=15, null=True)
    email = models.EmailField(null=True)
    message = models.TextField(max_length=15)

    def __str__(self):
        return str(self.user) + ' ' + str(self.names)

