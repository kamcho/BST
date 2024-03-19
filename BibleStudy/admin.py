from django.contrib import admin
from .models import AssignmentTaskProgress, JoinRequests, LocalBibleVersions, StudyGroups, GroupAssignment, CBR, TopicalBookMarks, BibleVersions, UserPreference, Books, Chapters, progress, BookMarks, Achievements, MyAchievements, KingJamesVersionI
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
admin.site.register(CBR)
admin.site.register(JoinRequests)
admin.site.register(KingJamesVersionI)
admin.site.register(LocalBibleVersions)
admin.site.register(GroupAssignment)
admin.site.register(AssignmentTaskProgress)