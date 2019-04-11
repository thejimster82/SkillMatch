"""skillmatch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
import os

from matching import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('about_us/', views.about_us, name='about_us'),
    path('matches/', include('matching.urls')),
    path('auth/', include('social_django.urls',
                          namespace='social')),  # for social auth
    path('', auth_views.LoginView.as_view(
        template_name='login.html'), name='login'),
    path('home/', views.home, name='home'),
    # path('update_match/<value>', views.update_match, name='update_match'),
    path('profile/<username>/edit/', views.update_profile, name='update_profile'),
    path('profile/<username>', views.profile, name='profile'),
    path('tutorprofile/<username>', views.tutorprofile, name='tutorprofile'),
    path('tutorprofile/<username>/becometutor', views.update_become_tutor,
         name='update_become_tutor'),
    path('tutorprofile/<username>/edit/',
         views.update_tutorprofile, name='update_tutorprofile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('search/', views.search, name='search'),
]
