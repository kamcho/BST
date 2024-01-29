from bs4 import BeautifulSoup
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
import requests
from django.contrib import messages
from Users.models import MyUser
from .models import StudyGroups, TopicalBookMarks, UserPreference, BibleVersions, Books, Chapters, progress, MyAchievements, BookMarks
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
        preference = UserPreference.objects.get(user=user)
        bibles = BibleVersions.objects.all()
        context['bibles'] = bibles
        context['preference'] = preference
        return context

    def post(self, *args, **kwargs):
        if self.request.method == 'POST':
            bible = self.request.POST.get('bible')
            bible = BibleVersions.objects.get(bible_id=bible)
            preference = self.get_context_data().get('preference')
            preference.default_bible = bible
            preference.save()



            return redirect(self.request.get_full_path())
        

class Read(TemplateView):
    template_name = 'BibleStudy/read.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bible_id = self.kwargs['bible_id']
        bible_id = BibleVersions.objects.get(name=bible_id)
        context['versions'] = BibleVersions.objects.all().order_by('name')
        context['books'] = Books.objects.all().order_by('-order')
        context['bible_uid'] = bible_id
        book = self.kwargs['book']
        book_count = Books.objects.get(name=book)
        book_name = book_count.book_id
        
        chapter = self.kwargs['chapter']
        bookapi = get_matthew_3(bible_id.bible_id,book_name, chapter)
        verse_count = bookapi[0]+1
        context['data'] = bookapi[1]
        count = list(range(1,book_count.chapters))
        context['count'] = count

        try:
            chapters = Chapters.objects.filter(book__name=book).order_by('order')
            context['chapters'] = chapters
            print(book,chapter ,'\n\n\n\n\n')
            chapter_id = Chapters.objects.get(book__name=book, order=chapter)
            print(book,chapter_id, chapter, '\n\n\n\n\n')
            context['chapter_id'] = chapter_id.id
        except Chapters.DoesNotExist:

            print('error\n\n\n')
            chapter_id = Chapters.objects.filter(book__name=book).order_by('order').first()
            if chapter_id:
                context['chapter_id'] = chapter_id.id
            else:
                context['chapter_id'] = 1
        
        
        return context
    
    def post(self, *args, **kwargs):
        if self.request.method == 'POST':
            bible_id = self.request.POST.get('bible')
            book = self.kwargs['book']



            return redirect(self.request.get_full_path())





def get_matthew_3(bible_id, book, chapter):
    api_key = '1cfeb0d5fb47d89b7bb6cef9e8427f6a'  # Replace 'YOUR_API_KEY' with your actual API key from bibleapi.co
    base_url = f'https://api.scripture.api.bible/v1/bibles/{bible_id}/chapters/{book}.{chapter}'

    headers = {'api-key': '0427945137760de29cd975e25a5b6e36'}

    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()  # Check for HTTP errors

        data = response.json()
      
        

        text_content = data['data']['content']
        print(text_content)

        count = (data['data']['verseCount'])
        

 
        return count, text_content

    except requests.exceptions.RequestException as err:

        print(f"Error fetching Bible verse: {str(err)}")
        return 10, 'NOT AVAILABLE. RELOAD'

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
            chapter = self.get_context_data().get('chapter')
            try:
                prog = progress.objects.get(book=chapter.book)
                prog.chapter.add(chapter)
            except progress.DoesNotExist:
                user = self.request.user
                prog = progress.objects.create(user=user, book=chapter.book)
                prog.chapter.add(chapter)


            return redirect('study-progress')
            



class StudyProgress(TemplateView):
    template_name = 'BibleStudy/study_progress.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        books = Books.objects.all().order_by('order')
        bible = UserPreference.objects.get(user=self.request.user)
        context['bible'] = bible
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

class MyBookMarks(TemplateView):
    template_name = 'BibleStudy/my_bookmarks.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['verses'] = BookMarks.objects.filter(user=user)

        return context

