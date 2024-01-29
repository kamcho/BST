from django.db import models

# Create your models here.
class DailyMessage(models.Model):
    date = models.DateField(auto_now=True)
    book = models.CharField(max_length=100)
    chapter = models.CharField(max_length=100)
    verse = models.CharField(max_length=100)
    word = models.TextField(max_length=1000)

    def __str__(self):
        return  str(self.book) + ' ' + str(self.chapter) + ' : ' + str(self.verse)