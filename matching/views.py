from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import User

from .forms import UserForm, ProfileForm
# Create your views here.


# def login(request):
#     return render(request, 'login.html')


def home(request):
    return render(request, 'home.html')


# def register(request):
#     if request.method == 'POST':
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('')
#     else:
#         form = UserCreationForm()

#         args = {'form': form}
#         return render(request, 'register.html', args)

@login_required
def update_profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        user_form = UserForm(request.POST, instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            return redirect(reverse('profile'))
    else:
        profile_form = ProfileForm(instance=request.user.profile)
        user_form = UserForm(instance=request.user)
    return render(request, 'update_profile.html', {
        'user_form' : user_form,
        'profile_form': profile_form,
    })

@login_required
def profile(request):
    user = User.objects.get(username = request.user.username)
    return render(request, 'profile.html', {
        "user":user,
        })