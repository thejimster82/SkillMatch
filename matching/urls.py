from django.urls import path
from . import views
from django.contrib.auth import logout, login

urlpatterns = [
    path('', views.profile, name='profile'),
    path('edit/', views.update_profile, name='update_profile'),
]