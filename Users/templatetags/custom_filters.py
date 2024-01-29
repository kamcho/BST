from bs4 import BeautifulSoup
from django import template
from django.db.models import Sum
import requests
from BibleStudy.models import progress, Chapters
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
def get_study_progress(book):
    try:
        prog = progress.objects.get(book__order=book)
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
def get_next_chapter(book):
    try:
        read = progress.objects.get(book__order=book)
        read_chapters = read.chapter.all()
        chapters = Chapters.objects.filter(book__order=book).exclude(id__in=read_chapters).order_by('order').first()
        if chapters:
            return chapters.order
        else:
            return 1
    except Exception as e:
        
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
def get_complete_count(book_id):
    print(book_id)
    prog = progress.objects.filter(book__book_id=book_id)
    total = prog.count()
    users = MyUser.objects.all().count()
    # print(total, users)
    read_count = (total / users) * 100

    return round(read_count)