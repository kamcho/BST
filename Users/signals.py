from django.db.models.signals import post_save
from django.dispatch import receiver
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
        

        
