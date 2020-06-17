from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('contactus/', views.contactUs, name='contactUs'),
    path('blogGrid/', views.blogGrid, name='blogGrid'),
    path('blogSingle/', views.blogSingle, name='blogSingle'),
    
]