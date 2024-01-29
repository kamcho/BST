from django.db import models

# Create your models here.

class Charity(models.Model):
    created = models.DateField(auto_now=True)
    closes_on = models.DateField()
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=3000)
    target = models.PositiveIntegerField()
    totals = models.PositiveIntegerField()
    archived = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title) + ' ' + str(self.target)

class ChurchProjects(models.Model):
    created = models.DateField(auto_now=True)
    closes_on = models.DateField()
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=3000)
    target = models.PositiveIntegerField()
    archived = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.title) + ' ' + str(self.target)
