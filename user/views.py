from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import User

from .forms import UserForm, ProfileForm

# Create your views here.
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





