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

    def testEmail(self):
        em = User.objects.get(username="a")
        self.assertEqual(em.email, "hehe@virginia.edu")

    def testUsername(self):
        em = User.objects.get(username="a")
        self.assertEqual(em.username, "a")

    def testFirstName(self):
        em = User.objects.get(username="a")
        self.assertEqual(em.first_name, "first")

    def testLastName(self):
        em = User.objects.get(username="a")
        self.assertEqual(em.last_name, "last")


class LoginTest(TestCase):

    def setUp(self):
        self.userProfile = User
        self.requestTest = RequestFactory()
        self.user1 = self.userProfile.objects.create_user(
            username="user1", email="user1@virginia.edu")
        self.server = UserSocialAuth.objects.create(
            user=self.user1, provider="google-oauth2", uid="1234")
        self.client = Client()

    def testSocialAuth(self):
        path = UserSocialAuth.objects.get_social_auth('google-oauth2', '1234')
        self.assertEqual(path, self.server)

    def testAuthorizedUser(self):
        self.client.force_login(self.user1)
        response = self.client.get('/matches/')
        self.assertEqual(response.status_code, 200)

    def testUnauthorizedUser(self):
        response = self.client.get('/matches/')
        self.assertEqual(response.status_code, 302)
