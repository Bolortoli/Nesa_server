from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('rewards/', views.rewards, name='rewards'),
    path('contactus/', views.contactUs, name='contactUs'),
]