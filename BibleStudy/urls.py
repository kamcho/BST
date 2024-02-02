from django.urls import path
from .views import Biblia, BookSelect, CreateStudyGroups, GroupDetails, GroupRequests, LeadersBoard, RequestStudyGroup, create_bookmark, TopicalBookMark, SetBiblePreference, Read, BooksAnalytics, MyBookMarks, StudyProgress, AddToGroup, SaveProgress, UsersAchievements, BibleStudyGroups
from . import views
urlpatterns = [

    path('<str:group_id>/Info/', GroupDetails.as_view(), name='group-id'),
    path('StudyGroups/', BibleStudyGroups.as_view(), name='study-groups'),
    path('Book-Analytics', BooksAnalytics.as_view(), name='book-analytics' ),
    path('Group/<str:group_id>/Add-Member', AddToGroup.as_view(), name='add-member'),
    path('Set-Bible-Preference/', SetBiblePreference.as_view(), name='set-bible-preference'),
    path('Study-Progress/', StudyProgress.as_view(), name='study-progress'),
    path('<str:bible_id>/<str:book>/<str:chapter>/', Read.as_view(), name='read'),
    path('Progress/<str:chapter_id>/Save', SaveProgress.as_view(), name='save-progress'),
    path('My-Achievements/', UsersAchievements.as_view(), name='achievements'),
    path('MyBookMarks/',MyBookMarks.as_view(), name='my-bookmarks'),
    path('BookMarks/<str:topic>/',TopicalBookMark.as_view(), name='bookmarks'),
    path('createBookmark/', views.create_bookmark, name='bookmark'),
    path('RequestStudyGroup/', RequestStudyGroup.as_view(), name='request-group'),
    path('JoinRequests/', GroupRequests.as_view(), name='join-requests'),
    path('LeadersBoard/', LeadersBoard.as_view(), name='leadersboard'),
    path('Biblia/', BookSelect.as_view(), name='biblia'),
    path('Biblia/<str:book>/<str:chapter>', Biblia.as_view(), name='read-biblia'),
    path('CreateGroup/', CreateStudyGroups.as_view(), name='create-group'),



]