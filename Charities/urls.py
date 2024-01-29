from django.urls import path
from .views import CreateCharity, CharityDetail, CharitiesView, ManageCharity, CreateProject, ProjectDetail, ProjectsView, ManageProject

urlpatterns = [

    path('Charitable-Projects/', CharitiesView.as_view(), name='charities'),
    path('Create-Charity/', CreateCharity.as_view(), name='create-charity'),
    path('Charity/<str:id>/', CharityDetail.as_view(), name='charity-id'),
    path('Manage/<str:charity_id>/', ManageCharity.as_view(), name='manage-charity'),


    path('Church-Projects/', ProjectsView.as_view(), name='projects'),
    path('Create-Church-Project/', CreateProject.as_view(), name='create-project'),
    path('<str:id>/', ProjectDetail.as_view(), name='project-id'),
    path('Church-Project/<str:project_id>/Manage', ManageProject.as_view(), name='manage-project'),



]