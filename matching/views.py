from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from .forms import UserForm, ProfileForm, BecomeTutorForm
from .models import Profile


@login_required
def home(request):
    user = User.objects.get(username=request.user.username)
    profile = Profile.objects.get(user=user)

    if (profile.first_login):
        profile.first_login = False
        profile.save()
        return redirect('update_profile')
    else:
        matches_list = profile.matches.all()
        return render(request, 'home.html', {
            'matches_list': matches_list
        })


@login_required
def update_profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=request.user.profile)
        user_form = UserForm(request.POST, request.FILES,
                             instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            return redirect(reverse('profile'))
    else:
        profile_form = ProfileForm(instance=request.user.profile)
        user_form = UserForm(instance=request.user)
    return render(request, 'update_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

@login_required
def update_become_tutor(request):
    if request.method == 'POST':
        become_tutor_form = BecomeTutorForm(request.POST, instance=request.user.profile)
        user_form = UserForm(request.POST, instance=request.user)
        if become_tutor_form.is_valid() and user_form.is_valid():
            become_tutor_form.save()
            user_form.save()
            return redirect(reverse('tutorprofile'))
    else:
        become_tutor_form = BecomeTutorForm(instance=request.user.profile)
        user_form = UserForm(instance=request.user)
    return render(request, 'update_become_tutor.html', {
        'user_form': user_form,
        'become_tutor_form': become_tutor_form,
    })


@login_required
def profile(request):
    user = User.objects.get(username=request.user.username)
    profile = Profile.objects.get(user=user)
    courses = profile.courses.all()
    return render(request, 'profile.html', {
        'user': user,
        'courses': courses,
    })

@login_required
def tutorprofile(request):
    user = User.objects.get(username=request.user.username)
    tutor_u = Profile.objects.get(user=user)
    tutor = tutor_u.tutor
    return render(request, 'tutorprofile.html', {
        "user": user,
        "tutor": tutor,
    })

@login_required
def matches(request):
    user = User.objects.get(username=request.user.username)
    profile = Profile.objects.get(user=user)
    matches_list = profile.matches.all()
    return render(request, 'matches.html', {
        'matches_list': matches_list,
    })


def search(request):
    if request.method == 'GET':  # If the form is submitted
        search_query = request.GET.get('search_box', None)
        print(search_query)
        results_list = Profile.objects.raw(
            "SELECT * from matching_profile where major LIKE %s", [search_query])
    return render(request, 'search.html', {
        'results_list': results_list,
    })
