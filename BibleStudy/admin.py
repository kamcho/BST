from django.contrib import admin
from .models import StudyGroups, TopicalBookMarks, BibleVersions, UserPreference, Books, Chapters, progress, BookMarks, Achievements, MyAchievements
# Register your models here.
admin.site.register(StudyGroups)
admin.site.register(BibleVersions)
admin.site.register(UserPreference)
admin.site.register(Books)
admin.site.register(Chapters)
admin.site.register(progress)
admin.site.register(Achievements)
admin.site.register(MyAchievements)
admin.site.register(BookMarks)
admin.site.register(TopicalBookMarks)