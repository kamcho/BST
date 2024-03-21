from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from Communication.models import Inbox
from .models import MyUser, PersonalProfile, UserTheme
from BibleStudy.models import UserPreference
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from allauth.socialaccount.signals import social_account_added

import json


@receiver(user_signed_up)
def update_user_profile(request, sociallogin, **kwargs):
    # sociallogin.user is the user instance
    user = sociallogin.user
    print(user)
    try:
        personal_profile, created = PersonalProfile.objects.get_or_create(user=user)
        personal_profile.f_name = sociallogin.account.extra_data.get('given_name', '')
        personal_profile.surname = sociallogin.account.extra_data.get('family_name', '')
        personal_profile.google_pic = sociallogin.account.extra_data.get('picture', '')
        personal_profile.save()


    except Exception as e:
        print(str(e))
    
    


@receiver(post_save,sender=MyUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        try:
            profile = PersonalProfile.objects.create(user=instance)
            theme = UserTheme.objects.create(user=instance)
            preference = UserPreference.objects.create(user=instance)
        except:
            pass
        

        
@receiver(post_save, sender=Inbox)
def send_email_notification(sender, instance, created, **kwargs):
    if created:
        subject = 'New Entry in Inbox'
        message = f'A new entry from {instance.email} at {instance.phone} has been added to the Inbox model.'
        recipient_email = ['njokevin999@gmail.com', 'njokevin9@gmail.com']  # Change this to your email address
        send_mail(subject, message, 'njokevin9@gmail.com', recipient_email)