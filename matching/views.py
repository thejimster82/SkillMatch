from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from .forms import UserForm, ProfileForm, TutorProfileForm, BecomeTutorForm
from .models import Profile


@login_required
def home(request):
    user = User.objects.get(username=request.user.username)
    profile = Profile.objects.get(user=user)

    if (profile.first_login):
        profile.first_login = False
        profile.save()
        return redirect('update_profile', username=user)
    else:
        matches_list = profile.matches.all()
        return render(request, 'home.html', {
            'matches_list': matches_list
        })
    
    
#added in the about us webpage request here
@login_required
def about_us(request):
    return render(request, 'about_us.html')


@login_required
def profile(request, username):
    user = User.objects.get(username=request.user.username)
    profile = Profile.objects.get(user=user)
    courses = profile.courses.all()
    return render(request, 'profile.html', {
        'user': user,
        'courses': courses,
    })


@login_required
def update_profile(request, username):
    user = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=request.user.profile)
        user_form = UserForm(request.POST, request.FILES,
                             instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            return redirect('profile', username=user)
    else:
        profile_form = ProfileForm(instance=request.user.profile)
        user_form = UserForm(instance=request.user)
    return render(request, 'update_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'user': user
    })


@login_required
def tutorprofile(request, username):
    user = User.objects.get(username=request.user.username)
    tutor_u = Profile.objects.get(user=user)
    tutor = tutor_u.tutor
    return render(request, 'tutorprofile.html', {
        "user": user,
        "tutor": tutor,
    })


@login_required
def update_become_tutor(request, username):
    user = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        become_tutor_form = BecomeTutorForm(
            request.POST, instance=request.user.profile)
        user_form = UserForm(request.POST, instance=request.user)
        if become_tutor_form.is_valid() and user_form.is_valid():
            become_tutor_form.save()
            user_form.save()
            return redirect('tutorprofile', username=user)
    else:
        become_tutor_form = BecomeTutorForm(instance=request.user.profile)
        user_form = UserForm(instance=request.user)
    return render(request, 'update_become_tutor.html', {
        'user_form': user_form,
        'become_tutor_form': become_tutor_form,
    })


@login_required
def update_tutorprofile(request, username):
    user = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        tutorprofile_form = TutorProfileForm(
            request.POST, request.FILES, instance=request.user.profile)
        user_form = UserForm(request.POST, request.FILES,
                             instance=request.user)
        if tutorprofile_form.is_valid() and user_form.is_valid():
            tutorprofile_form.save()
            user_form.save()
            return redirect('tutorprofile', username=user)
    else:
        tutorprofile_form = TutorProfileForm(instance=request.user.profile)
        user_form = UserForm(instance=request.user)
    return render(request, 'update_tutorprofile.html', {
        'user_form': user_form,
        'tutorprofile_form': tutorprofile_form,
    })


@login_required
def matches(request):
    user = User.objects.get(username=request.user.username)
    profile = Profile.objects.get(user=user)
    matches_list = profile.matches.all()
    return render(request, 'matches.html', {
        'matches_list': matches_list,
    })

@login_required
def tutors(request):
    tutor_list = Profile.objects.filter(tutor=True)
    return render(request, 'tutors.html', {'tutor_list': tutor_list})

def search(request):
    if request.method == 'GET':  # If the form is submitted
        search_query = request.GET.get('search_box', None)
        print(search_query)
        results_list = Profile.objects.raw(
            "SELECT * from auth_User where username LIKE %s", ['%'+search_query+'%'])
    return render(request, 'search.html', {
        'results_list': results_list,
    })