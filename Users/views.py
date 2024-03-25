from allauth.socialaccount.models import SocialAccount
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.contrib.auth import logout
from django.core.cache import cache

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db.models import Count, Q
from django.shortcuts import redirect, get_object_or_404, render
from django.views.generic import TemplateView
from BibleStudy.models import BibleVersions, KingJamesVersionI, Books, Chapters, StudyGroups, UserPreference, progress, Chapters
from Communication.models import MessagingSettings
from DailyWord.models import DailyMessage
from django.db.models import Sum
from Users.models import PersonalProfile, MyUser
import logging

logger = logging.getLogger('django')

from django.contrib.sitemaps import Sitemap
from django.urls import reverse


# views.py
# views.py

from .models import MyUser, PersonalProfile, UserTheme

from django.contrib.auth.hashers import make_password


       


    
class StaticViewSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.9

    def items(self):
        return ['register', 'student-home', 'login', 'leadersboard','contact-us' ]  # Add the names of your static views

    def location(self, item):
        return reverse(item)
    

    
# @method_decorator(cache_page(60 * 500), name='dispatch')
class RegisterView(TemplateView):
    template_name = "Users/register.html"

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            email = request.POST.get('email')
            pwd1 = request.POST.get('pwd1')
            pwd2 = request.POST.get('pwd2')
            role = 'Member'

            if email and pwd2 and pwd1:
                if pwd2 == pwd1:
                    try:
                        user = MyUser.objects.create_user(email=email, role=role, password=pwd1)
                        user.save()

                        messages.success(request, f'Account for {email} has been created successfully.')
                        
                        user = authenticate(self.request, username=email, password=pwd1)

                        if user is not None:
                            # Log the user in
                            login(self.request, user)
                            # Redirect to a success page
                            return redirect('edit-profile')
                        else:
                            return redirect('login')

                            

                    except IntegrityError as e:
                        messages.error(request, f'A user with the email {email} already exists!')
                else:
                    messages.error(request, 'The passwords did not match!')
            else:
                messages.error(request, 'You did not completely fill out the form.')

        return redirect(request.get_full_path())



# @method_decorator(cache_page(60 * 500), name='dispatch')
class Login(TemplateView):
    template_name = 'Users/login.html'

    def post(self, *args, **kwargs):
        if self.request.method == 'POST':
            # Create an instance of the AuthenticationForm and populate it with user-submitted data

            username = self.request.POST.get('email')
            password = self.request.POST.get('password')
            user = authenticate(self.request, username=username, password=password)

            if user is not None:
                # Log the user in
                login(self.request, user)
                # Redirect to a success page
                return redirect('redirect')
            else:
                # Return an error message if authentication fails
                messages.error(self.request, "Invalid username or password. Try again !")
                return redirect(self.request.get_full_path())

def logout_view(request):
    logout(request)

    return render(request, 'Users/logout.html')
class MyProfile(LoginRequiredMixin, TemplateView):
    """
        view and manipulate a user's profile.
        Attach a learner to your watch list for parents/guardians
    """
    template_name = "Users/profile.html"

    def get_context_data(self, **kwargs):
        context = super(MyProfile, self).get_context_data(**kwargs)
        user = self.request.user
        try:
            group = StudyGroups.objects.get(members=user)
            context['group'] = group
            theme = UserTheme.objects.get(user=user)
            context['theme'] = theme
        except StudyGroups.DoesNotExist:
            messages.error(self.request, 'You are currently not in any group. Please wait as we find one for you !')
        except UserTheme.DoesNotExist:
            # messages.info(self.request, 'Set your theme verse.')
            pass
        read_percentage = progress.objects.filter(user=user)
        chapters_count = read_percentage.aggregate(total=Count('chapter'))['total']
        
        if chapters_count:
            chapters = Chapters.objects.all().count()
            prog = (chapters_count / chapters) * 100
            context['progress'] = round(prog)
        else:
            context['progress'] = 0


        return context

    def post(self, args, **kwargs):
        # Check for Post requests
        if self.request.method == "POST":
            user = self.request.user
            # Check which button is clicked
            if 'profile' in self.request.POST:
                try:

                        # Get logged in user's profile for editing
                        profile = PersonalProfile.objects.get(user=user)  # get users personal profile
                        f_name = self.request.POST.get('first-name').lower()
                        new_phone_number = self.request.POST.get('phone-number')
                        l_name = self.request.POST.get('last-name').lower()
                        surname = self.request.POST.get('surname').lower()
                        gender = self.request.POST.get('gender')
                        uploaded_file = self.request.FILES.get('photo')
                        dob = self.request.POST.get('dob')
                        if new_phone_number:
                            profile.phone = new_phone_number
                        profile.f_name = f_name
                        profile.l_name = l_name
                        profile.gender = gender
                        profile.surname = surname
                        if uploaded_file:

                            profile.profile_pic = uploaded_file
                        # profile.dob = dob
                        profile.save()
                        messages.success(self.request, 'Profile has been successfully Updated!')

                except PersonalProfile.DoesNotExist as e:
                    # Create personal profile if none is found
                    messages.error(self.request, 'OOOps that did not work, Please try again!!')
                    personal_profile = PersonalProfile.objects.create(user=user)

                except IntegrityError:
                    messages.error(self.request, 'A user with this phone number already exists !! If this number belongs to you contact @support')

                except Exception as e:
                    # Handle any unhandled errors
                    messages.error(self.request, f'{str(e)}')
                    error_message = str(e)  # Get the error message as a string
                    error_type = type(e).__name__

                    logger.critical(
                        error_message,
                        exc_info=True,  # Include exception info in the log message
                        extra={
                            'app_name': __name__,
                            'url': self.request.get_full_path(),
                            'school': settings.SCHOOL_ID,
                            'error_type': error_type,
                            'user': self.request.user,
                            'level': 'Critical',
                            'model': 'Database Error',
                        }
                    )

                # # Add a learner to a guardians watch list
            
        return redirect(self.request.get_full_path())


class LoginRedirect(LoginRequiredMixin, TemplateView):
    """
        Redirect a user based on their role
    """
    template_name = 'Users/login_redirect.html'

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        try:
            user = self.request.user
            role = user.role
            profile = self.request.user.personalprofile
            f_name = profile.f_name
        except PersonalProfile.DoesNotExist as e:
            profile = PersonalProfile.objects.create(user=user)
            f_name = profile.f_name
        

        except Exception as e:
            error_message = str(e)  # Get the error message as a string
            error_type = type(e).__name__

            logger.critical(
                error_message,
                exc_info=True,  # Include exception info in the log message
                extra={
                    'app_name': __name__,
                    'url': self.request.get_full_path(),
                    'school': settings.SCHOOL_ID,
                    'error_type': error_type,
                    'user': self.request.user,
                    'level': 'Warning',
                    'model': 'DatabaseError',
                }
            )
        finally:
            try:
                bible = UserPreference.objects.get(user=user)

            except UserPreference.DoesNotExist:
                bible = None

            # If a user has not updated their profile redirect them to profile editing page
            if f_name == '':
                return redirect('edit-profile')
            elif f_name !=  '' and not bible:
                return redirect('set-bible-preference')
            else:
                
                return redirect('student-home')
                
        
                
               


def finish_profile_setup(user, f_name, l_name, surname, phone, gender, dob):
 
    profile = PersonalProfile.objects.get(user=user)
    profile.f_name = f_name
    profile.l_name = l_name
    profile.gender = gender
    profile.dob = dob
    if phone:
        profile.phone = phone
    profile.surname = surname
    profile.save()
    return None


class FinishSetup(LoginRequiredMixin, TemplateView):
    """
        User's profile edit Page, mainly for first time account users
    """
    template_name = 'Users/edit_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            pass

        except:
            context['base_html'] = 'Users/base.html'
            messages.error(self.request, 'Not logged in')


        return context

    def post(self, request, **kwargs):
        if request.method == 'POST':
            f_name = request.POST.get('f_name').lower()
            l_name = request.POST.get('l_name').lower()
            surname = request.POST.get('surname').lower()
            phone = request.POST.get('phone')
            gender = request.POST.get('gender')
            dob = request.POST.get('dob')
            print(dob, '\n\n\n\n')
            user = self.request.user  # get user from session.

            try:
                # Get user's profile for editing
                if self.request.user.role == 'Admin':
                    messages.error(self.request, 'You can only use the admin interface')
                    return redirect('logout')
                if f_name and l_name and surname:
                    finish_profile_setup(user=user, f_name=f_name, l_name=l_name, surname=surname, phone=phone, gender=gender, dob=dob)


            # if no profile matching query is found, create it and update it
            except PersonalProfile.DoesNotExist as e:
                PersonalProfile.objects.create(user=user, dob=dob)
                finish_profile_setup(user=user, f_name=f_name, l_name=l_name, surname=surname, phone=phone, gender=gender, dob=dob)

            except IntegrityError:
                messages.error(self.request, 'A user with this phone number already exists !! If this number belongs to you contact @support')
            



            except Exception as e:
                messages.error(request, 'We could not process your request, try again.!!')
                error_message = str(e)  # Get the error message as a string
                error_type = type(e).__name__

                logger.critical(
                    error_message,
                    exc_info=True,  # Include exception info in the log message
                    extra={
                        'app_name': __name__,
                        'url': self.request.get_full_path(),
                        'school': settings.SCHOOL_ID,
                        'error_type': error_type,
                        'user': self.request.user,
                        'level': 'Critical',
                        'model': 'DatabaseError',
                    }
                )
                return redirect(request.get_full_path())

            # Finally reroute a user based on their role
            finally:
                try:
                    pref = UserPreference.objects.get(user=user)

                    return redirect('students-home')
                except:
                    return redirect('set-bible-preference')
            
        else:
            return redirect(request.get_full_path())

    # ensure a user is only editing their profile.
    def test_func(self):
        user = self.request.user
        profile = get_object_or_404(PersonalProfile, user=user)
        return profile.user == user  # Check if the profile belongs to the logged-in user


def rout(request):
    try:
        role = request.user.role
        print(role)

        if role == 'Guardian':
            return redirect('guardian-home')
        elif role == 'Member':
            return redirect('student-home')
        elif role == 'Teacher':
            return redirect('teacher-home')
        elif role == 'Partner':
            return redirect('partner-home')
        elif role in ['Finance', 'Supervisor']:
            return redirect('supervisor-home')
    except:
        return redirect('logout')

class Home(TemplateView):
    """
    Home view for the Student's dashboard.
    Displays the user's progress and related information.
    """
    template_name = 'Users/home.html'

    def get_context_data(self, **kwargs):
        """
        Populate the context with data for the template.
        """
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            try:
                user = self.request.user
                group = StudyGroups.objects.get(members=user)
                context['group'] = group
            except StudyGroups.DoesNotExist:
                if user.is_authenticated:
                    
                    messages.info(self.request, 'You have not yet been assigned a bible study group yet!')
                          
            read_percentage = progress.objects.filter(user=user)
            chapters_count = read_percentage.aggregate(total=Count('chapter'))['total']
            if chapters_count:
                chapters = Chapters.objects.all().count()
                prog = (chapters_count / chapters) * 100
                context['progress'] = round(prog)

        else:
            messages.info(self.request, 'Sign In to join a bible study group')
        word = cache.get('cached_daily_message')  # Check if the data is already cached
        if not word:
            word = DailyMessage.objects.order_by('-id').first()  # Retrieve the latest DailyMessage
            cache.set('cached_daily_message', word, timeout=82800)  # Cache the data for 1 hour
        context['word'] = word
        


        return context
    
    def test_func(self):
        try:
            role = self.request.user.role
            return role        
        except:
            return False

    
        
class Settings(LoginRequiredMixin, TemplateView):
    template_name = 'Users/settings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        bibles = BibleVersions.objects.all()
        context['bibles'] = bibles
        try:
            setting = MessagingSettings.objects.get(user=user)
            context['settings'] = setting
        except:
            pass

        try:
            preference = UserPreference.objects.get(user=user)
            
            context['preference'] = preference
        except UserPreference.DoesNotExist:
            pass
        try:
            theme = UserTheme.objects.get(user=user)
            context['theme'] = theme
        except:
            pass
        

        return context 
    
    def post(self,*args, **kwargs):
        if self.request.method == 'POST':
            user = self.request.user
            if 'verify' in self.request.POST:
                book = self.request.POST.get('book')
                chapter = self.request.POST.get('chapter')
                verse = self.request.POST.get('verse')
                theme = get_theme_verse(book, chapter, verse)
                user_theme = self.get_context_data().get('theme')
                if theme is False:
                    theme = None
                    messages.error(self.request, 'This bible verse does not exist')
                else:
                    user_theme.book = book
                    user_theme.chapter = chapter
                    user_theme.verse = verse
                    user_theme.word = theme
                    user_theme.save()
                    messages.success(self.request, 'Theme updated succesfully')

                context = {
                    'verse':theme,
                    'books':self.get_context_data().get('books'),
                    'theme':user_theme
                }
                
            
            elif 'biblia' in self.request.POST:
                bible = self.request.POST.get('bible')
                
                try:
                    bible = BibleVersions.objects.get(bible_id=bible)
                    preference = self.get_context_data().get('preference')
                    preference.default_bible = bible
                    preference.save()
                    messages.success(self.request, 'Success!')
                    
                except AttributeError:
                    preference = UserPreference.objects.create(user=user, default_bible=bible)
                    messages.success(self.request, 'Success!')

            elif 'daily-target' in self.request.POST:
                target = self.request.POST.get('target')
                try:
                    
                    preference = self.get_context_data().get('preference')
                    preference.daily_target = target
                    preference.save()
                    messages.success(self.request, 'Success!')
                    
                except AttributeError:
                    user = self.request.user
                    preference = UserPreference.objects.create(user=user, daily_target=target)
                    messages.success(self.request, 'Success!')

            else:
                user = self.request.user
                # sms = self.request.POST.get('sms')
                tasapp = self.request.POST.get('whatsapp')
                try:
                    messaging = MessagingSettings.objects.get(user=user)
                except MessagingSettings.DoesNotExist:
                    messaging = MessagingSettings.objects.create(user=user)
                # sms = bool(sms)
                tasapp = bool(tasapp)

                # messaging.sms = sms
                messaging.whatsapp = tasapp
                messaging.save()

            return redirect(self.request.get_full_path())


            
        

def get_theme_verse(book, chapter, verse):
    book = Books.objects.get(name=book)
    verse = KingJamesVersionI.objects.get(book=book.order, chapter=chapter, verse=verse)

    return verse.text
    