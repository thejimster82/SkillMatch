import operator
from datetime import datetime

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import reverse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.db.models import Q
from django.utils.six.moves import reduce

from .forms import UserForm, ProfileForm, ProfileCoursesForm, TutorProfileForm, BecomeTutorForm
from .models import Profile, MatchesTable, Course


def card_processed(user_a, user_b):
    return MatchesTable.objects.filter(from_user=user_a, to_user=user_b).exists()


def match_exists(user_a, user_b):
    mutual = MatchesTable.objects.filter(
        from_user=user_a, to_user=user_b, like=True).exists() and MatchesTable.objects.filter(
            from_user=user_b, to_user=user_a, like=True).exists()
    return mutual


@login_required
def home(request):
    user = request.user
    profile = request.user.profile

    if (profile.first_login):
        profile.first_login = False
        profile.save()
        return redirect('update_profile', username=user)

    if request.method == 'POST':
        seconduser = User.objects.get(username=request.POST['r_id'])
        if 'accept' in request.POST:
            MatchesTable.objects.create(
                from_user=user, to_user=seconduser, like=True)
            seconduser.profile.rank += 1
            seconduser.profile.save()
        if 'reject' in request.POST:
            MatchesTable.objects.create(
                from_user=user, to_user=seconduser, like=False)

    course_filter = Q(profile__courses__in=profile.courses.all())
    all_matches = User.objects.filter(course_filter).distinct()

    match_filter = [~Q(username=request.user.username)]
    for match in all_matches:
        if card_processed(user, match):
            match_filter.append(~Q(username=match.username))
    new_match = all_matches.filter(reduce(operator.iand, match_filter))[0:1]
    finished = not new_match.exists()

    return render(request, 'home.html', {
        'user': user,
        'match': new_match,
        'finished': finished
    })



@login_required
def matches(request):
    user = User.objects.get(username=request.user.username)
    profile = Profile.objects.get(user=user)
    all_matches = MatchesTable.objects.filter(from_user=user)

    if request.method == 'POST':
        seconduser = User.objects.get(username=request.POST['r_id'])
        if 'Delete Match' in request.POST:
            t = all_matches.filter(to_user=seconduser).values_list('id', flat=True)
            match = MatchesTable.objects.get(id = t[0])
            match.like = False
            match.save()

    match_filter = [Q()]
    for match in all_matches:
        if match_exists(user, match.to_user):
            match_filter.append(Q(to_user=match.to_user))
    valid_matches = all_matches.filter(reduce(operator.ior, match_filter))



    return render(request, 'matches.html', {
        'matches_list': valid_matches,
    })


@login_required
def about_us(request):
    return render(request, 'about_us.html')


@login_required
def profile(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    courses = profile.courses.all()
    tutor_u = Profile.objects.get(user=user)
    tutor = tutor_u.tutor
    return render(request, 'profile.html', {
        'user': user,
        'courses': courses,
        "tutor": tutor,
    })


def graduation_range():
    now = datetime.now().year
    return (2019, now + 4)


@login_required
def update_profile(request, username):
    UserForm(instance=request.user)
    user = User.objects.get(username=request.user.username)
    grad_range = graduation_range()
    if request.method == 'POST':
        profile_form = ProfileForm(
            request.POST, request.FILES, instance=request.user.profile)
        user_form = UserForm(request.POST, request.FILES,
                             instance=request.user)
        course_form = ProfileCoursesForm(
            request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid() and user_form.is_valid() and course_form.is_valid():
            profile_form.save()
            user_form.save()
            course_form.save()
            return redirect('profile', username=user.username)
    else:
        profile_form = ProfileForm(
            instance=user.profile)
        user_form = UserForm(instance=user)
        course_form = ProfileCoursesForm(instance=user.profile)
    return render(request, 'update_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'course_form': course_form,
        'user': user
    })


@login_required
def tutorprofile(request, username):
    user = User.objects.get(username=request.user.username)
    tutor_u = Profile.objects.get(user=user)
    tutor = tutor_u.tutor
    return render(request, 'profile.html', {
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
    if request.method == 'POST':
        tutorprofile_form = TutorProfileForm(
            request.POST, request.FILES, instance=request.user.profile)
        user_form = UserForm(request.POST, request.FILES,
                             instance=request.user)
        if tutorprofile_form.is_valid() and user_form.is_valid():
            tutorprofile_form.save()
            user_form.save()
            return redirect('tutorprofile', username=request.user.username)
    else:
        tutorprofile_form = TutorProfileForm(instance=request.user.profile)
        user_form = UserForm(instance=request.user)
    return render(request, 'update_tutorprofile.html', {
        'username': request.user.username,
        'user_form': user_form,
        'tutorprofile_form': tutorprofile_form,
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
            "SELECT * from auth_User where username ILIKE %s", ['%' + search_query + '%'])
        results_list_name = Profile.objects.raw(
            "SELECT * from auth_User where first_name ILIKE %s", ['%' + search_query + '%'])
        results_list_major = Profile.objects.raw(
            "SELECT * from matching_profile where major ILIKE %s", ['%' + search_query + '%'])
        searched_course = Course.objects.raw(
            "SELECT * from matching_course where course_title ILIKE %s", ['%' + search_query + '%'])
        searched_course_profile_list = []
        for tmp_cs in searched_course:
            for tmp_user in tmp_cs.profile_set.all():
                if tmp_user not in searched_course_profile_list:
                    searched_course_profile_list.append(tmp_user)
        print(searched_course_profile_list)
    return render(request, 'search.html', {
        'results_list': results_list,
        'results_list_major': results_list_major,
        'results_list_name': results_list_name,
        'results_list_courses': searched_course_profile_list,
    })
