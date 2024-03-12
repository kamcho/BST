from django.urls import path
from .views import CreateWord, WordDetail

urlpatterns = [

    path('Create-Daily-Word/', CreateWord.as_view(), name='create-word'),
    path('<str:word_id>/', WordDetail.as_view(), name='word-detail'),



]