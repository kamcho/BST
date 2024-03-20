from bs4 import BeautifulSoup
from django import template
from django.db.models import Sum, Count
import requests
from BibleStudy.models import AssignmentTaskProgress, BibleVersesASV, BibleVersesKJV, BibleVersesSwahili, GroupAssignment, KingJamesVersionI, Books, progress, Chapters
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
        print(percentage)

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
        if read.chapter.count() == chapter_count :
            return 'True'
        if chapters:
            print(chapters)
            return chapters.order
        else:
            return 1
    except Exception as e:
        # print(str(e))
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
    chapters = Chapters.objects.filter(book__name=book)
    # chapters = [i for i in range(1, chapters + 1)]
    # chapters = {
    #     'chapter':chapters,
    #     'id':book
    # }

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
def get_read_percent(user, location):
    print(location)
    if location == 'bible':
        total_chapters = progress.objects.filter(user=user).values('chapter').annotate(num_chapters=Count('chapter')).aggregate(total=Count('chapter'))
        percent = (total_chapters['total'] / 1189) * 100
        if percent < 1 and percent > 0:
            percent = 1
    elif location == 'OT':
        total_chapters = progress.objects.filter(user=user, book__location='OT').values('chapter').annotate(num_chapters=Count('chapter')).aggregate(total=Count('chapter'))
        percent = (total_chapters['total'] / 929) * 100
        print(percent)
        if percent < 1 and percent > 0:
            percent = 1
    else:
        total_chapters = progress.objects.filter(user=user, book__location='NT').values('chapter').annotate(num_chapters=Count('chapter')).aggregate(total=Count('chapter'))
        percent = (total_chapters['total'] / 260) * 100
        if percent < 1 and percent > 0:
            percent = 1



    return round(percent)
        
@register.filter
def get_book_verse(book, chapter):
    try:
        verses = KingJamesVersionI.objects.filter(book=book,chapter=chapter)
        return verses
    except KingJamesVersionI.DoesNotExist:
        return None
    
@register.filter
def get_chapter(chapter):
    try:
        chapter = Chapters.objects.get(id=chapter)
        return chapter
    except :
        return None


@register.filter
def get_verses(book,chapter):
    verses = BibleVersesKJV.objects.filter(book=book, chapter=chapter)

    return verses


@register.simple_tag
def get_text(bible_id, book, chapter, verse):
    
    try:
        if bible_id == '0001':
            text = BibleVersesASV.objects.get(book=book, chapter=chapter, verse=verse)
        elif bible_id == '0002':
            text = BibleVersesKJV.objects.get(book=book, chapter=chapter, verse=verse)

        # elif bible_id == '0003':
        #     text = BibleVersesSwahili.objects.get(book=book, chapter=chapter, verse=verse)
        else:
            text = BibleVersesASV.objects.get(book=book, chapter=chapter, verse=verse)
            return text.text
    except:
        return 'Not Found'
    return text.text
@register.simple_tag
def save_passes_test(user, book, chapter):
    try:
        print(user, book, chapter)
        try:
            prog = progress.objects.get(user=user, book__name=book, chapter__order=chapter)

            return "Saved"
        except:
            try:
            
                prog = progress.objects.get(user=user, book__name=book)
                last_chapter = prog.chapter
                is_complete = prog.book.chapters
        
                if is_complete == last_chapter.count():

                    return None
                
                
                else:
                    if (last_chapter.count() + 1) == int(chapter):
                        print('True')
                        return True
                    else:
                        print('False')
                        return False    
            except:
                return chapter == '1'
                
        
                
        
            
       

    except progress.DoesNotExist:
        return True
    



@register.simple_tag
def check_task_done(test, user, chapter):
    print(test, user, chapter)
    try:
        is_done = AssignmentTaskProgress.objects.get(user=user, task=test, chapters=chapter)
        return True
    except:
        return False
    
@register.simple_tag
def check_user_task_done(test, user):
    print(test, user)
    if test != '0':
        try:
            is_done = AssignmentTaskProgress.objects.get(user=user, task=test)
            done = is_done.chapters.count()
            totals = GroupAssignment.objects.get(id=test)
            totals = totals.chapters.count()
            percentage = (done / totals)*100
            return round(percentage)
        except:
            return 0
        
    return ''