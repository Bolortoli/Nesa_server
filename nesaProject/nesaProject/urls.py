"""nesaProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
    

urlpatterns = [
    re_path(r'^jet/', include('jet.urls', 'jet')),
    re_path(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')), 
    re_path(r'^admin/', admin.site.urls),
    re_path('', include('nesa.urls')),
    re_path(r'^', include(('social_django.urls', 'social'), namespace='social'), name='social'),
    re_path(r'^', include(('nesa.urls', 'auth'), namespace='auth'), name='auth'),
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
