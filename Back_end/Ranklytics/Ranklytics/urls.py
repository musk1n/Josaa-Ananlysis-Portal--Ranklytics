"""
URL configuration for Ranklytics project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from home.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', home,name="home"),
    
    path('about/', about,name="about"),
    path('lletsbegin/', slider,name="slider"),
    
    path('display_choices/',display_choices,name="display_choices"),
    path('popular_branches/',plot_graph,name="popular_branches"),
    path('college_popular_branch/',college_branch_popularity,name="college_branch_popularity"),
    path('branch_college_popularity/', branch_college_popularity, name='branch_college_popularity'),
    path('branch-college-trend/', branch_college_trend, name='branch_college_trend'),
    path('new-branches-popularity/', new_branches_popularity, name='new_branches_popularity'),
  
   
     path('predict/',preference_view, name='preference_view'),




]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

