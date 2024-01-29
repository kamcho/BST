from django.shortcuts import redirect, render
from BibleStudy.models import Books
from django.contrib import messages

from Users.views import get_theme_verse
from .models import DailyMessage
from django.views.generic import TemplateView
# Create your views here.


class CreateWord(TemplateView):
    template_name = 'DailyWord/create_word.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Books.objects.all().order_by('order')
        return context

    def post(self, *args, **kwargs):
        if self.request.method == 'POST':
            book = self.request.POST.get('book')
            chapter = self.request.POST.get('chapter')
            verse = self.request.POST.get('verse')
            print(book, chapter, verse)
            if 'verify' in self.request.POST:
                print('verify')

                word = get_theme_verse(book, chapter, verse)
                if word:
                    self.request.session['word'] = word

                    context = {
                        'verse':word,
                        'books':self.get_context_data().get('books')
                    }
                    return render(self.request, self.template_name, context)
                else:
                    messages.error(self.request, 'We could not find a verse mathing your queerry. Try again !!')
                return redirect(self.request.get_full_path())
            elif 'save' in self.request.POST:
                try:
                    word = self.request.session.get('word')

                    word = DailyMessage.objects.create(book=book, chapter=chapter, verse=verse, word=word)
                    return redirect('word-detail', word.id)
                except Exception:
                    messages.error(self.request, 'OOOOOPS!!. The system couldnt create Daily Word. Try Again !!')
                    return redirect(self.request.get_full_path())
            
            else:
                return redirect(self.request.get_full_path())

            
        
class WordDetail(TemplateView):
    template_name = 'DailyWord/word_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        word = self.kwargs['word_id']
        word = DailyMessage.objects.get(id=word)
        context['word'] = word
        return context
    
    def post(self, *args, **kwargs):
        if self.request.method == 'POST':
            try:
                word = self.get_context_data().get('word')
                word.delete()
                messages.success(self.request, 'Succesfully Deleted Daily Word')

                return redirect('create-word')
            except Exception:
                messages.success(self.request, 'An error occurred! Try again !!')

                return redirect(self.request.get_full_path())

