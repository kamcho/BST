from django.urls import path
from .views import DonateToCharity

urlpatterns = [

    path('<str:instance>/<str:charity_id>/Donate/', DonateToCharity.as_view(), name='donate'),
   


]