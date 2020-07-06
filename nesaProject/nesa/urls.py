from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('logindex', views.logindex, name='logindex'),
    path('contactus/', views.contactUs, name='contactUs'),
    path('rewards-blog-archive/', views.rewardsBlogArchive, name='rewards-blog-archive'),
    path('rewards-blog-single/', views.rewardsBlogSingle, name='rewards-blog-single'),
    path('rewards-blog-grid/', views.rewardsBlogGrid, name='rewards-blog-grid'),
    path('news-blog-archive/', views.newsBlogArchive, name='news-blog-archive'),
    path('news-blog-single/', views.newsBlogSingle, name='news-blog-single'),
]