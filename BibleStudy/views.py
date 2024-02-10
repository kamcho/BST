import datetime as datetime
from itertools import groupby
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from .tester import get_verses
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models, connection
# from .tester import add_verse
from operator import attrgetter
from django.db.models import F, Window
import requests
from bs4 import BeautifulSoup
from django.utils.safestring import mark_safe
from django.db.models.functions import DenseRank
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
import requests
from django.db.models import Count
from django.contrib import messages
from Communication.models import Inbox
from Users.models import MyUser, PersonalProfile
from .models import CBR, Achievements, KingJamesVersionI, JoinRequests, StudyGroups, TopicalBookMarks, UserPreference, BibleVersions, Books, Chapters, progress, MyAchievements, BookMarks
# Create your views here.

uskey = 'd6ce6236fb09203ed8356c4b04c6bd78'


BASE_URL = 'https://api.bible/v1/bibles'

def get_bible_names():
    headers = {'api-key': uskey}
    response = requests.get(BASE_URL, headers=headers)

    if response.status_code == 200:
        data = response.json()
        # Assuming the Bible names are under the 'data' key
        bible_names = [bible['name'] for bible in data.get('data', [])]
        return bible_names
    else:
        print(f"Failed to fetch Bible names. Status code: {response.status_code}")
        return None


class CreateStudyGroups(TemplateView):
    template_name = 'BibleStudy/create_group.html'

    def post(self, *args, **kwargs):
        if self.request.method == 'POST':
            name = self.request.POST.get('name').lower()
            try:
                group = StudyGroups.objects.create(group_name=name)

                return redirect('group-id', group.group_id)
            except :
                messages.error(self.request, f'A group with name {name} already exists! Try another name.')

                return redirect(self.request.get_full_path())




class BibleStudyGroups(TemplateView):
    template_name = 'BibleStudy/study_groups.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = StudyGroups.objects.all()

        return context

class AddToGroup(TemplateView):
    template_name = 'BibleStudy/add_to_studygroup.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group_id = self.kwargs['group_id']
        context['group'] = StudyGroups.objects.get(group_id=group_id)
        context['users'] = MyUser.objects.all().order_by('email')


        return context 
    
    def post(self, *args, **kwargs):
        if self.request.method == 'POST':
            user = self.request.POST.get('user')
            leader = self.request.POST.get('pastor')
            if  leader:
                user = MyUser.objects.get(email=user)
                group = self.get_context_data().get('group')
                group.group_leader = user
                group.members.add(user)
                group.save()
                messages.success(self.request, f'Succesfully made {user} as {group.group_name} group leader.')
                

            else:
                user = MyUser.objects.get(email=user)
                group = self.get_context_data().get('group')
                group.members.add(user)
                messages.success(self.request, f'Succesfully added {user} to {group.group_name} Bible Study.')
                

            
            return redirect('group-id',group.group_id)




class GroupDetails(TemplateView):
    template_name = 'BibleStudy/group_id.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        group_id = self.kwargs['group_id']
        group = StudyGroups.objects.get(group_id=group_id)
        context['group'] = group
        return context

class SetBiblePreference(TemplateView):
    template_name = 'BibleStudy/set_bible_preference.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        bibles = BibleVersions.objects.all()
        context['bibles'] = bibles
        try:
            preference = UserPreference.objects.get(user=user)
            
            context['preference'] = preference
        except UserPreference.DoesNotExist:
            pass
        
        
        return context

    def post(self, *args, **kwargs):
        if self.request.method == 'POST':
            bible = self.request.POST.get('bible')
            user = self.request.user
            try:
                bible = BibleVersions.objects.get(bible_id=bible)
                preference = self.get_context_data().get('preference')
                preference.default_bible = bible
                preference.save()
                messages.success(self.request, 'Success!')
                
            except AttributeError:
                preference = UserPreference.objects.create(user=user, default_bible=bible)
                messages.success(self.request, 'Success!')






            return redirect('student-home')
def get_all_books():
    
    books = Books.objects.all()
    print(books)
    for book in books:
        post_chapter(book)
    

def post_chapter(book):
    base_url = 'https://api.scripture.api.bible/v1/bibles'
    endpoint = f'{base_url}/de4e12af7f28f599-02/books/{book.book_id}/chapters'

    headers = {
        'api-key': '1cfeb0d5fb47d89b7bb6cef9e8427f6a',
    }
    try:
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()  # Raise an exception for bad requests

        # Assuming the API returns data in JSON format
        books_data = response.json()['data']
        # print(books_data)
        for data in books_data:
            try:
                data = int(data['number'])
                # print(data)
                chapter = Chapters.objects.create(book=book, order=data)

            except:
                print('intro')

        # Extract books from the response
        books = books_data
    

        return None

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

def get__post_books(bible_id):
    base_url = 'https://api.scripture.api.bible/v1/bibles'
    endpoint = f'{base_url}/06125adad2d5898a-01/books'

    headers = {
        'api-key': '1cfeb0d5fb47d89b7bb6cef9e8427f6a',
    }
    
    try:
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()
        response = response.json()
        books = response['data']
        count = 1
        for book in books:
            Books.objects.create(name=book['name'], order=count, book_id=book['id'],
                                  abbreviation=book['abbreviation'],location='OT', chapters=0)
            
            count+=1
           
    except Exception as e:
        print(str(e))
@method_decorator(cache_page(60 * 500), name='dispatch')
class BookSelect(TemplateView):
    template_name = 'BibleStudy/biblia.html'
  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        books = Books.objects.all().order_by('order')
        context['books'] = books
               
 
        print(books)

        return context
    

# @method_decorator(cache_page(60 * 500), name='dispatch')
class Biblia(TemplateView):
    template_name = 'BibleStudy/read_biblia.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.kwargs['book']
        
        # context['data'] = get_verses()
        book = Books.objects.get(name=book)
        context['book'] = book.order
        chapter = self.kwargs['chapter']
        chapters = Chapters.objects.filter(book__name=book)
        context['chapters'] = chapters
        context['focus'] = chapter
        get__post_books()
        # add_vers_e()
        
        


        return context

def get_book_verse(book, chapter):
    try:
        verses = KingJamesVersionI.objects.filter(book=book,chapter=chapter)
        return verses
    except KingJamesVersionI.DoesNotExist:
        return None

def get_bible_verse_by_id(book, chapter):
    verses = KingJamesVersionI.objects.filter(book=book, chapter=chapter)

    return verses

@method_decorator(cache_page(60 * 500), name='dispatch')
class Read(TemplateView):
    template_name = 'BibleStudy/read.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bible_id = self.kwargs['bible_id']
        chapter = self.kwargs['chapter']
        bible_id = BibleVersions.objects.get(name=bible_id)
        context['versions'] = BibleVersions.objects.all().order_by('name')
        context['books'] = Books.objects.all().order_by('-order')
        context['bible_uid'] = bible_id
        book = self.kwargs['book']
        book_count = Books.objects.get(name=book)
        book_name = book_count.book_id
        context['data'] = get_verses(bible_id.bible_id, book_name,chapter)
        
        
        # verse = get_bible_verse_by_id(book_count.order, chapter)
        # context['data']  = verse

        try:
            chapter_id = Chapters.objects.get(book__name=book, order=chapter)
            context['chapter_id'] = chapter_id.id
        except Chapters.DoesNotExist:

            print('error\n\n\n')
            chapter_id = Chapters.objects.filter(book__name=book).order_by('order').first()
            if chapter_id:
                context['chapter_id'] = chapter_id.id
            else:
                context['chapter_id'] = 1
        
        
        return context
    
    








class SaveProgress(TemplateView):
    template_name = 'BibleStudy/save_progress.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chapter_id = self.kwargs['chapter_id']
        chapter = Chapters.objects.get(id=chapter_id)
        context['chapter'] = chapter

        return context
    
    def post(self, *args, **kwargs):
        if self.request.method == 'POST':
            user = self.request.user
            chapter = self.get_context_data().get('chapter')
            try:
                prog = progress.objects.get(user=user, book=chapter.book)
                prog.chapter.add(chapter)
            except progress.DoesNotExist:
                
                prog = progress.objects.create(user=user, book=chapter.book)
                prog.chapter.add(chapter)

            award_points(user)
            create_achievement(user)


            return redirect('study-progress')
            
def award_points(user):
    
    date = datetime.date.today()
    cbr, created = CBR.objects.get_or_create(user=user, date=date)
    cbr.read_count = cbr.read_count + 1
    cbr.save()

    try:
        preference = UserPreference.objects.get(user=user)
    except UserPreference.DoesNotExist:
        bible = BibleVersions.objects.filter(language='English').first()
        preference = UserPreference.objects.create(user=user, default_bible=bible)

    target = preference.daily_target
    if target == cbr.read_count:
        profile = PersonalProfile.objects.get(user=user)
        profile.points = profile.points + 100
        profile.save()

    return None


def create_achievement(user):
    print('Myuser',user)
    total_chapters = progress.objects.filter(user=user).values('chapter').annotate(num_chapters=Count('chapter')).aggregate(total=Count('chapter'))
    raw_percent = (total_chapters['total'] / 10) * 100
    try:
        percent = round(raw_percent)
        print(percent)
        
        if percent > 12 and percent < 25:            
            achievement = Achievements.objects.get(identifier__gte=12, identifier__lt=25)
            achievements = MyAchievements.objects.create(user=user, achievement=achievement)
        elif percent > 24 and percent < 50:
            achievement = Achievements.objects.get(identifier__gte=24, identifier__lt=50)
            achievements = MyAchievements.objects.create(user=user, achievement=achievement)
        elif percent > 49 and percent < 75:
            achievement = Achievements.objects.get(identifier__gte=49, identifier__lt=75)
            achievements = MyAchievements.objects.create(user=user, achievement=achievement)
        elif percent > 74 and percent < 90:
            achievement = Achievements.objects.get(identifier__gte=74, identifier__lt=90)
            achievements = MyAchievements.objects.create(user=user, achievement=achievement)
        elif percent > 89 and percent < 100:
            achievement = Achievements.objects.get(identifier__gte=89, identifier__lt=100)
            achievements = MyAchievements.objects.create(user=user, achievement=achievement)
        elif raw_percent == 100:
            achievement = Achievements.objects.get(identifier=raw_percent)
            achievements = MyAchievements.objects.create(user=user, achievement=achievement)
        
        try:
            points = PersonalProfile.objects.get(user=user)
            points.points += achievement.points
            points.save()
        except:
            pass
    except Exception as e:
        print(str(e))
    return None

class StudyProgress(LoginRequiredMixin,TemplateView):
    template_name = 'BibleStudy/study_progress.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        books = Books.objects.all().order_by('order')
        try:
            bible = UserPreference.objects.get(user=self.request.user)
            context['bible'] = bible
        except UserPreference.DoesNotExist:
            bible = BibleVersions.objects.filter(language='English').first()
            context['default_bible'] = bible
            
        context['books'] = books

        return context
    
    def post(self, *args, **kwargs):
        if self.request.method == 'POST':
            if 'new' in self.request.POST:
                books = Books.objects.filter(location='NT').order_by('order')
                context = {
                    'bible':self.get_context_data().get('bible'),
                    'books':books,
                    'location':'New Testament'
                }
                return render(self.request, self.template_name, context)
            elif 'old' in self.request.POST:
                books = Books.objects.filter(location='OT').order_by('order')
                context = {
                    'bible':self.get_context_data().get('bible'),
                    'books':books,
                    'location':'Old Testament'

                }
                return render(self.request, self.template_name, context)
                
            else:
                return redirect(self.request.get_full_path())

            




class UsersAchievements(TemplateView):
    template_name = 'BibleStudy/my_achievements.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        achievements = MyAchievements.objects.filter(user=user)
        if not achievements:
            messages.info(self.request, 'Begin to study the bible to unlock achievements!')
        context['achievements'] = achievements

        return context


class BooksAnalytics(TemplateView):
    template_name = 'BibleStudy/books_analytics.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        prog = progress.objects.all()
        by_book = prog.values('book__name', 'book__book_id').order_by('book_id', 'book')
        # .distinct('book')

        context['books'] = by_book


        return context
    
@method_decorator(cache_page(60 * 500), name='dispatch')
class TopicalBookMark(TemplateView):
    template_name = 'BibleStudy/bookmarks.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topic = self.kwargs['topic']
        if topic == 'all':
            bm = TopicalBookMarks.objects.all()
        else:
            bm = TopicalBookMarks.objects.filter(topic=topic)
            
        context['verses'] = bm

        return context
    




def create_bookmark(request):
    
    print('hello wrld \n\n\n\n\n')
    book = request.POST.get('book')
    chapter = request.POST.get('chapter')
    verse = request.POST.get('verse_id')
    user = request.POST.get('user')
    print(verse)
    # text = KingJamesVersionI.objects.get(book)

    if verse:
        # Convert user_id to an integer

        # Check if the user is authenticated (you can modify this logic as needed)
    

        # Create a bookmark
        user = request.user
        bookmark = BookMarks.objects.create(
            user=user,
            verse=f"{book} {chapter}:{verse}",
            word='text',
        )

        # Optionally, return additional data in the JSON response
        return JsonResponse({'success': True, 'message': 'Bookmark created successfully'})
        
    else:
        # Handle the case when user_id or verse_id is not provided
        return JsonResponse({'success': False, 'message': 'user_id or verse_id not provided'})


class MyBookMarks(LoginRequiredMixin, TemplateView):
    template_name = 'BibleStudy/my_bookmarks.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        verses = BookMarks.objects.filter(user=user)
        context['verses'] = verses
        if not verses:
            messages.info(self.request, 'You do not have any bookmarked verses.')

        return context


class GroupRequests(TemplateView):
    template_name = 'BibleStudy/requests_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['requests'] = JoinRequests.objects.all().order_by('date')

        return context
    
    def post(self, *args, **kwargs):
        if self.request.method == 'POST':
            user = self.request.user
            clicked = self.request.POST.get('clicked')
            group = StudyGroups.objects.get(group_name=clicked)
            group.members.add(user)
            messages.success(self.request, 'Success')

            return redirect(self.request.get_full_path())



class RequestStudyGroup(TemplateView):
    template_name = 'BibleStudy/request_group.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = StudyGroups.objects.annotate(num_members=Count('members')).filter(num_members__lt=8)
        return context
    
    def post(self, *args, **kwargs):
        if self.request.method == 'POST':
            group = self.request.POST.get('group')
            group = StudyGroups.objects.get(group_name=group)
            user = self.request.user
            try:
                join_request = JoinRequests.objects.create(user=user, group=group)
                messages.success(self.request, 'We have received your request, Please wait for approval.')
            except Exception as e :
                messages.info(self.request, f'We already received your request, Please wait for approval.!!')

            return redirect('student-home')


def assign_group(user):
    # Assuming 'user' is the user for whom you want to assign a group
    user_gender = user.personalprofile.gender  # Assuming you have a 'PersonalProfile' associated with the user

    # Get all StudyGroups with less than 8 members
    eligible_groups = StudyGroups.objects.annotate(num_members=Count('members')).filter(num_members__lt=8)

    # If there are eligible groups, find the one with the least members of the user's gender
    if eligible_groups.exists():
        sorted_groups = sorted(eligible_groups, key=lambda group: group.members.filter(personalprofile__gender=user_gender).count())
        selected_group = sorted_groups[0]

        # Add the user to the selected group
        selected_group.members.add(user)



class LeadersBoard(TemplateView):
    template_name = 'BibleStudy/leadersboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profiles = list(PersonalProfile.objects.all().order_by('-points'))

# Iterate through the profiles and assign ranks
        profiles = list(PersonalProfile.objects.all().order_by('-points'))

# Initialize variables
        ranked_profiles = []
        current_rank = 0

        # Group profiles by points
        for points, group in groupby(profiles, key=attrgetter('points')):
            points_group = list(group)

            # Assign the same rank to profiles with the same points
            for profile in points_group:
                profile.rank = current_rank + 1

            # Skip the following rank
            current_rank += len(points_group)

            # Append profiles to the result list
            ranked_profiles.extend(points_group)



        context['profiles'] = ranked_profiles
        current_user = self.request.user  # Replace with your actual way of getting the current user

# Find the rank of the current user
        if current_user:
            current_user_profile = next((profile for profile in ranked_profiles if profile.user == current_user), None)
            current_user_rank = current_user_profile.rank if current_user_profile else None
            context['rank'] = current_user_rank

        return context



def create_books_from_api(api_response):
    for index, book_data in enumerate(api_response, start=1):
        # Extracting data from the API response
        name = book_data['name']
        abbreviation = book_data['abbreviation']
        book_id = book_data['id']
        location = 'NT' if index > 39 else 'OT'  # Assuming 39 is the number of books in the Old Testament
        order = index
        chapters = 0  # You can set the actual number of chapters if available in the API response

        # Creating a Book object
        book = Books.objects.create(
            name=name,
            abbreviation=abbreviation,
            book_id=book_id,
            location=location,
            order=order,
            chapters=chapters
        )

        print(f"Book '{book}' created successfully!")

# def get_verses():
#     base_url = 'https://api.scripture.api.bible/v1/bibles'
#     endpoint = f'{base_url}/de4e12af7f28f599-02/chapters/GEN.1'

#     headers = {
#         'api-key': '1cfeb0d5fb47d89b7bb6cef9e8427f6a',
#     }
    
#     try:
#         response = requests.get(endpoint, headers=headers)
#         response.raise_for_status()

#         # Assuming the API returns data in JSON format
#         books_data = response.json()['data']['content']
#         return books_data

#     except requests.exceptions.RequestException as e:
#         print(f"Error: {e}")
#         return None



class ContactUs(TemplateView):
    template_name = 'BibleStudy/contact_us.html'

    def post(self, *args, **kwargs):
        if self.request.method == 'POST':
            names = self.request.POST.get('names')
            phone = self.request.POST.get('phone-number')
            mail = self.request.POST.get('mail')
            about = self.request.POST.get('about')
            message = self.request.POST.get('message')
            if self.request.user.is_authenticated:
                user = self.request.user
            else:
                user = None
            inbox = Inbox.objects.create(user=user, names=names, phone=phone,
                                          email=mail, about=about, message=message)
            messages.success(self.request, 'We have received your message, we will get back to you ASAP!')
            return redirect(self.request.get_full_path())