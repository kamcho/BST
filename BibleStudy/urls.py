from django.urls import path
from .views import GroupDetails, TopicalBookMark, SetBiblePreference, Read, BooksAnalytics, MyBookMarks, StudyProgress, AddToGroup, SaveProgress, UsersAchievements, BibleStudyGroups

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



]