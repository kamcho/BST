from django.db import models

# Create your models here.
import uuid

from django.db import models
from datetime import datetime,timedelta

from django.urls import reverse
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


# from Teacher.models import SchoolClass


class MyUserManager(BaseUserManager):
    def create_user(self, email, role, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """

        user = self.model(


            email=email,
            role=role,



        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(

            email=email,
            role='Admin',
            # uuid=uuid.uuid4(),
            password=password,

        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    class Role(models.TextChoices):
        Member = "Member"
        Pastor = "Pastor"
        ADMIN = "ADMINISTRATOR"
        Supervisor = "Supervisor"


    base_role = Role.Member
    email = models.EmailField(unique=True)
    uuid = models.CharField(max_length=100, default=uuid.uuid4, unique=True)
    role = models.CharField(max_length=15, choices=Role.choices, default=base_role)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = MyUserManager()
    USERNAME_FIELD = 'email'


    def __str__(self):
        return str(self.email)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class MemberManager(BaseUserManager):
    def get_queryset(self,*args,**kwargs):
        result = super().get_queryset(*args,**kwargs)
        return result.filter(role=MyUser.Role.Member)


class Member(MyUser):
    base_role = MyUser.Role.Member
    member = MemberManager()

    class Meta:
        proxy = True




class PastorManager(BaseUserManager):
    def get_queryset(self,*args,**kwargs):
        result = super().get_queryset(*args,**kwargs)
        return result.filter(role=MyUser.Role.Pastor)


class Pastor(MyUser):
    base_role = MyUser.Role.Pastor
    pastor = PastorManager()

    class Meta:
        proxy = True



class SupervisorManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        result = super().get_queryset(*args, **kwargs)
        return result.filter(role=MyUser.Role.Supervisor)


class Supervisor(MyUser):
    base_role = MyUser.Role.Supervisor
    partner = SupervisorManager()

    class Meta:
        proxy = True

# class FinanceManager(BaseUserManager):
#     def get_queryset(self, *args, **kwargs):
#         result = super().get_queryset(*args, **kwargs)
#         return result.filter(role=MyUser.Role.Finance)


# class Finance(MyUser):
#     base_role = MyUser.Role.Finance
#     partner = FinanceManager()

#     class Meta:
#         proxy = True

class UserTheme(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    book = models.CharField(max_length=100)
    chapter = models.PositiveIntegerField()
    verse = models.PositiveIntegerField()
    word = models.TextField(max_length=300)

    def __str__(self):
        return str(self.user)
    
def get_chapters(book):
    chapters = chapters.objects.filter(book__name=book)

    return chapters
    

    
class PersonalProfile(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    f_name = models.CharField(max_length=30)
    ref_id = models.CharField(max_length=100, blank=True)
    dob = models.DateField()
    l_name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30, blank=True)
    profile_pic = models.FileField(upload_to='ProfilePics/', default='ProfilePics/realistic-black-background-with-realistic-elements_23-2149156849.avif')
    google_pic = models.CharField(max_length=300,null=True)
    gender = models.CharField(max_length=10, blank=True)
    phone = models.CharField(max_length=15, null=True)
    points = models.PositiveIntegerField(default=50)

    def __str__(self):
        return self.user.email
    





