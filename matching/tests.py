from django.test import TestCase, RequestFactory, Client
from .models import Profile
from django.contrib.auth.models import User
from social_django.models import UserSocialAuth
from .forms import UserForm, ProfileForm
from .views import update_profile, profile

# Create your tests here.

# creating user test, check the information stored in User is correct or not


class CreateUser(TestCase):

    def setUp(self):
        User.objects.create(username="a", email="hehe@virginia.edu",
                            first_name="first", last_name="last")

    def test_email(self):
        em = User.objects.get(username="a")
        self.assertEqual(em.email, "hehe@virginia.edu")

    def test_username(self):
        em = User.objects.get(username="a")
        self.assertEqual(em.username, "a")

    def test_first_name(self):
        em = User.objects.get(username="a")
        self.assertEqual(em.first_name, "first")

    def test_last_name(self):
        em = User.objects.get(username="a")
        self.assertEqual(em.last_name, "last")


class LoginTest(TestCase):

    def setUp(self):
        self.userProfile = User
        self.requestTest = RequestFactory()
        self.user1 = self.userProfile.objects.create_user(
            username="user1", email="user1@virginia.edu")
        self.profile = Profile.objects.get(user=self.userProfile)
        self.server = UserSocialAuth.objects.create(
            user=self.user1, provider="google-oauth2", uid="1234")
        self.client = Client()

    def test_social_auth(self):
        path = UserSocialAuth.objects.get_social_auth('google-oauth2', '1234')
        self.assertEqual(path, self.server)

    def test_authorized_user(self):
        self.client.force_login(self.user1)
        response = self.client.get('/matches/')
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_user(self):
        response = self.client.get('/matches/')
        self.assertEqual(response.status_code, 302)

    def test_first_login_true(self):
        self.profile.first_login = True
        self.profile.save()
        response = self.client.get('/home/')
        self.assertRedirects(response, 'profile/edit/')

    def test_first_login_false(self):
        self.profile.first_login = False
        self.profile.save()
        response = self.client.get('/home/')
        self.assertTemplateUsed('home.html')


class MatchesTest(TestCase):

    def setUp(self):
        u1 = User.objects.create(
            username="b", email="test1@virginia.edu", first_name="first1", last_name="last1")
        p1 = Profile.objects.get(user=u1)

        u2 = User.objects.create(
            username="c", email="test2@virginia.edu", first_name="first2", last_name="last2")
        p2 = Profile.objects.get(user=u2)

        p1.matches.add(p2)

    def test_has_match(self):
        u1 = User.objects.get(username='b')
        p1 = Profile.objects.get(user=u1)
        self.assertQuerysetEqual(p1.matches.all(), ['<Profile: c>'])

    def test_no_matches(self):
        u2 = User.objects.get(username="c")
        p2 = Profile.objects.get(user=u2)
        self.assertFalse(p2.matches.all().exists())
