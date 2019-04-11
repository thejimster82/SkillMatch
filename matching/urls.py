from django.urls import path
from . import views
from django.contrib.auth import logout, login

urlpatterns = [
    path('', views.matches, name='matches')
]
