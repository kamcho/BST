import uuid
from django.db import models

from Users.models import MyUser

class BibleVersesKJV(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.PositiveSmallIntegerField()
    chapter = models.PositiveSmallIntegerField()
    verse = models.PositiveSmallIntegerField()
    text = models.TextField()

    class Meta:
        db_table = 'bible_verses_kjv'
        managed = False

class BibleVersesASV(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.PositiveSmallIntegerField()
    chapter = models.PositiveSmallIntegerField()
    verse = models.PositiveSmallIntegerField()
    text = models.TextField()

    class Meta:
        db_table = 'bible_verses_asv'
        managed = False

class BibleVersesSwahili(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.PositiveSmallIntegerField()
    chapter = models.PositiveSmallIntegerField()
    verse = models.PositiveSmallIntegerField()
    text = models.TextField()

    class Meta:
        db_table = 'bible_verses_swahili'
        managed = False
# Create your models here.
class KingJamesVersionI(models.Model):

    book = models.PositiveSmallIntegerField()
    chapter = models.PositiveSmallIntegerField()
    verse = models.PositiveSmallIntegerField()
    text = models.TextField()

    def __str__(self):
        return str(self.book) + ' ' + str(self.chapter) + ' ' + str(self.verse) 
    
    class Meta:
        unique_together = ('book','chapter','verse')



class Books(models.Model):
    choices = (
        ('NT', 'NT'),
        ('OT', 'OT')
    )
    name = models.CharField(max_length=100, unique=True)
    book_id = models.CharField(max_length=30, unique=True)
    abbreviation = models.CharField(max_length=30, null=True)
    location = models.CharField(max_length=15, choices=choices)
    order = models.PositiveIntegerField(unique=True)
    chapters = models.PositiveIntegerField()

    def __str__(self):
        return str(self.name)
    


class Chapters(models.Model):
    book = models.ForeignKey(Books, related_name='book', on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    def __str__(self):
        return str(self.book) + ' ' + str(self.order)
    class Meta:
        unique_together = ('book','order')
    
class progress(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    chapter = models.ManyToManyField(Chapters)

    def __str__(self):
        return str(self.user)
    class Meta:
        unique_together = ('user','book')
    
class TopicalBookMarks(models.Model):
    choices = (
        ('Faith','Faith'),
        ('Sin','Sin'),
        ('Sorrow','Sorrow'),
        ('Thanks Giving', 'Thanks Giving'),
        ('Giving', 'Giving'),
        ('Living', 'Living'),
        ('Forgiving', 'Forgiving'),
        ('Encouragement', 'Encouragement')
    )
    topic = models.CharField(max_length=100, choices=choices)
    verse = models.CharField(max_length=30)
    word = models.TextField(max_length=1000, default='None')

    def __str__(self):
        return str(self.verse)

class BookMarks(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    book = models.CharField(max_length=30, null=True)
    chapter = models.CharField(max_length=30, null=True)
    verse = models.CharField(max_length=30)
    word = models.TextField(max_length=1000, default='None')

    def __str__(self):
        return str(self.user)





class LocalBibleVersions(models.Model):
    choices = (
        ('English','English'),
        ('Kikuyu', 'Kikuyu'),
        ('Swahili', 'Swahili'),
        ('Luo', 'Luo'), 
    )
    name = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    bible_id = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)



class BibleVersions(models.Model):
    choices = (
        ('English','English'),
        ('Kikuyu', 'Kikuyu'),
        ('Swahili', 'Swahili'),
        ('Luo', 'Luo'), 
    )
    name = models.CharField(max_length=100)
    language = models.CharField(max_length=100)
    bible_id = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)


class UserPreference(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    default_bible = models.ForeignKey(BibleVersions, null=True, on_delete=models.CASCADE)
    profile_visibility = models.BooleanField(default=True)
    daily_target = models.PositiveIntegerField(default=5)

    def __str__(self):
        return str(self.user)


class StudyGroups(models.Model):
    group_id = models.UUIDField(unique=True,primary_key=True, default=uuid.uuid4)
    group_name = models.CharField(max_length=100, unique=True)
    group_leader = models.ForeignKey(MyUser, null=True, on_delete=models.CASCADE)
    members = models.ManyToManyField(MyUser, related_name='members')

    def __str__(self):
        return str(self.group_name)
    
class JoinRequests(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    group = models.ForeignKey(StudyGroups, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)
    
    class Meta:
        unique_together = ('user', 'group')


    

class Achievements(models.Model):
    identifier = models.PositiveIntegerField(default=12)
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    points = models.PositiveIntegerField()

    def __str__(self):
        return str(self.name)
    
class MyAchievements(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievements, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)
    
    class Meta:
        unique_together = ('user', 'achievement')
    


class CBR(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    read_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.user)
    
    class Meta:
        unique_together = ('user','date')
    