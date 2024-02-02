from bs4 import BeautifulSoup
from django import template
from django.db.models import Sum, Count
import requests
from BibleStudy.models import BibleVersesKJV, Books, progress, Chapters
from Users.models import MyUser
from Payments.models import CharityPayments, ProjectPayments
register = template.Library()



@register.filter
def divide(value, arg):
    try:
        if value is not None and arg is not None:
            value = int(value)
            arg = int(arg)
            return round((arg / value) * 100)
        else:
            return 0
    except (ValueError, ZeroDivisionError):
        return 0
    
@register.filter
def get_progress(total, charity_id):
    contributions = CharityPayments.objects.filter(charity__id=charity_id)
    try:
        totals = contributions.aggregate(totals=Sum('amount'))['totals']
        print('\n\n\n\n\n', totals)
        if totals != 0:
            percentage = (totals / total)*100
            percentage = round(percentage)
            return percentage
        else :
            return 0
    except:
        return 0
    
@register.filter
def get_project_progress(total, project_id):
    contributions = ProjectPayments.objects.filter(project__id=project_id)
    try:
        totals = contributions.aggregate(totals=Sum('amount'))['totals']
        print('\n\n\n\n\n', totals)
        if totals != 0:
            percentage = (totals / total)*100
            percentage = round(percentage)
            return percentage
        else :
            return 0
    except:
        return 0
    

@register.filter
def get_study_progress(user, book):
    try:
        prog = progress.objects.get(user=user, book__order=book)
        chapters_covered = prog.chapter.count()
        percentage = (chapters_covered / prog.chapter.first().book.chapters) * 100

        return round(percentage)
    except :
        
        return None
    

# user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
#     book = models.ForeignKey(Books, on_delete=models.CASCADE)
#     chapter = models.ManyToManyField(Chapters)

#     def __str__(self):
#         return str(self.user)

@register.filter
def get_next_chapter(user, book):
    try:
        read = progress.objects.get(user=user, book__order=book)
        book_id = Books.objects.get(order=book)
        chapter_count = book_id.chapters
        
        read_chapters = read.chapter.all()
        chapters = Chapters.objects.filter(book__order=book).exclude(id__in=read_chapters).order_by('order').first()
        print(book_id.name,chapter_count,read.chapter.count(), chapters.order)
        if read.chapter.count() == chapter_count :
            return 'True'
        if chapters:
            return chapters.order
        else:
            return 1
    except:
        return 1
    

    

@register.simple_tag
def get_matthew_3(bible_id, chapter_id, verse_id):
    base_url = f'https://api.scripture.api.bible/v1/bibles/{bible_id}/verses/{chapter_id}.{verse_id}'

    headers = {'api-key': '0427945137760de29cd975e25a5b6e36',
               
               }

    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()  # Check for HTTP errors

        data = response.json()
        

        html_content = data['data']['content']
        soup = BeautifulSoup(html_content, 'html.parser')
        text_content = soup.get_text(separator=' ', strip=True)

        print(text_content)

        return text_content

    except requests.exceptions.RequestException as err:
        print(f"Error fetching Bible verse: {err}")




@register.filter
def get_read_count(book_id):
    print(book_id)
    prog = progress.objects.filter(book__book_id=book_id)
    total = prog.count()
    users = MyUser.objects.all().count()
    # print(total, users)
    read_count = (total / users) * 100

    return round(read_count)

@register.filter
def get_chapters(book):
    chapters = Chapters.objects.filter(book__name=book).count()
    chapters = [i for i in range(1, chapters + 1)]

    return chapters

@register.filter
def get_complete_count(book_id):
    print(book_id)
    prog = progress.objects.filter(book__book_id=book_id)
    total = prog.count()
    users = MyUser.objects.all().count()
    # print(total, users)
    read_count = (total / users) * 100

    return round(read_count)

@register.filter
def get_read_percent(user,location):
    print(location)
    if location == 'bible':
        total_chapters = progress.objects.filter(user=user).values('chapter').annotate(num_chapters=Count('chapter')).aggregate(total=Count('chapter'))
        percent = (total_chapters['total'] / 1189) * 100
        if percent < 1 and percent > 0:
            percent = 1
    elif location == 'OT':
        total_chapters = progress.objects.filter(user=user, book__location='OT').values('chapter').annotate(num_chapters=Count('chapter')).aggregate(total=Count('chapter'))
        percent = (total_chapters['total'] / 39) * 100
        if percent < 1 and percent > 0:
            percent = 1
    else:
        total_chapters = progress.objects.filter(user=user, book__location='NT').values('chapter').annotate(num_chapters=Count('chapter')).aggregate(total=Count('chapter'))
        percent = (total_chapters['total'] / 27) * 100
        if percent < 1 and percent > 0:
            percent = 1



    return round(percent)
        
@register.filter
def get_book_verse(book, chapter):
    try:
        verses = BibleVersesKJV.objects.filter(book=book,chapter=chapter)
        return verses
    except BibleVersesKJV.DoesNotExist:
        return None