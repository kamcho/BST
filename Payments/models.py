from django.db import models
from Charities.models import Charity, ChurchProjects

from Users.models import MyUser


# Create your models here.

class InitiatedPayments(models.Model):
    choices = (
        ('Charity','Charity'),
        ('Project', 'Project'),
        ('Offering', 'Offering')
    )
    checkout_id = models.CharField(max_length=100)
    object_id = models.CharField(max_length=30, null=True)
    purpose = models.CharField(max_length=30)
    time = models.DateTimeField(auto_now=True)
    amount = models.PositiveIntegerField()
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)
    
class ProjectPayments(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    project = models.ForeignKey(ChurchProjects, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    date = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.user)

    


class CharityPayments(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    charity = models.ForeignKey(Charity, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    date = models.DateField(auto_now=True)

    def __str__(self):
        return str(self.user)