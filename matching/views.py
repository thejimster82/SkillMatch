from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic

from .forms import UserForm, ProfileForm
from .models import Profile
# Create your views here.


def home(request):
    return render(request, 'home.html')


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
        'user_form': user_form,
        'profile_form': profile_form,
    })


@login_required
def profile(request):
    user = User.objects.get(username=request.user.username)
    return render(request, 'profile.html', {
        "user": user,
    })


@login_required
def matches(request):
    # I am having trouble accessing the matches ManyToMany field
    user = User.objects.get(username=request.user.username)
    #matches_list = user.profile.matches.all()
    profile = Profile.objects.get(user=user)
    matches_list = profile.matches.all()
    return render(request, 'matches.html', {
        'matches_list': matches_list,
    })


# class MatchesView(LoginRequiredMixin, generic.ListView):
#    model = Profile
#    template_name = 'matches.html'
#    context_object_name = 'matches_list'
#
#    def get_queryset(self):
#        return Profile.matches.all()
