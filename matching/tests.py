from django.test import TestCase, RequestFactory, Client
from .models import Profile, Course
from django.contrib.auth.models import User
from social_django.models import UserSocialAuth
from .forms import UserForm, ProfileForm
from .views import update_profile, profile

# Create your tests here.
# EDIT PROFILE TEST


class EditProfileTest(TestCase):
    def setUp(self):
        self.requestTest = RequestFactory()
        self.user1 = User.objects.create(username="1", email="test1@virginia.edu",
                                         first_name="first1", last_name="last1")
        User.objects.create(username="2", email="test2@virginia.edu",
                            first_name="first2", last_name="last2")
        self.profile = Profile.objects.get(user=self.user1)
        self.server = UserSocialAuth.objects.create(
            user=self.user1, provider="google-oauth2", uid="1234")
        self.client = Client()

    def test_editBtn(self):
        response = self.client.get('/profile/2')
        buttonString = "Edit Profile</button>"
        self.assertTrue(buttonString not in response.content)

# PROFILE TESTS


class CreateUserTest(TestCase):

    def setUp(self):
        User.objects.create(username="a", email="test@virginia.edu",
                            first_name="first", last_name="last")

    def test_email(self):
        em = User.objects.get(username="a")
        self.assertEqual(em.email, "test@virginia.edu")

    def test_username(self):
        em = User.objects.get(username="a")
        self.assertEqual(em.username, "a")

    def test_first_name(self):
        em = User.objects.get(username="a")
        self.assertEqual(em.first_name, "first")

    def test_last_name(self):
        em = User.objects.get(username="a")
        self.assertEqual(em.last_name, "last")

# LOGIN TESTS


class LoginTest(TestCase):

    def setUp(self):
        self.requestTest = RequestFactory()
        self.user1 = User.objects.create(
            username="user1", email="user1@virginia.edu")
        self.profile = Profile.objects.get(user=self.user1)
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
        self.assertTemplateNotUsed('home.html')

    def test_first_login_false(self):
        self.profile.first_login = False
        self.profile.save()
        response = self.client.get('/home/')
        self.assertTemplateUsed('home.html')

# MATCHING TESTS


class MatchesTest(TestCase):

    def setUp(self):
        u1 = User.objects.create(
            username="b", email="test1@virginia.edu", first_name="first1", last_name="last1")
        p1 = Profile.objects.get(user=u1)

        u2 = User.objects.create(
            username="c", email="test2@virginia.edu", first_name="first2", last_name="last2")
        p2 = Profile.objects.get(user=u2)

        p1.matches.add(u2)

    def test_has_match(self):
        u1 = User.objects.get(username='b')
        p1 = Profile.objects.get(user=u1)
        self.assertQuerysetEqual(p1.matches.all(), ['<User: c>'])

    def test_no_matches(self):
        u2 = User.objects.get(username="c")
        p2 = Profile.objects.get(user=u2)
        self.assertFalse(p2.matches.all().exists())

# SEARCHING TESTS


class SearchTest(TestCase):

    def setUp(self):
        u1 = User.objects.create(username="b", first_name="first1")
        p1 = Profile.objects.get(user=u1)
        p1.major = "major1"
        p1.save()

        # u2 = User.objects.create(username="c", first_name="first2")
        # p2 = Profile.objects.get(user=u2)
        # p2.major = "major2"

        course1 = Course.objects.create(course_title="course1")
        # course2 = Course.objects.create(course_title="course2")

        p1.courses.add(course1)
        # p2.courses.add(course1)
        # p2.courses.add(course2)

    def test_search_by_username(self):
        search_query = 'b'
        results_list = Profile.objects.raw(
            "SELECT * from auth_User where username LIKE %s COLLATE utf8_general_ci", ['%' + search_query + '%'])
        self.assertEquals(results_list[0].username, 'b')

    def test_search_by_first_name(self):
        search_query = "first1"
        results_list_name = Profile.objects.raw(
            "SELECT * from auth_User where first_name LIKE %s COLLATE utf8_general_ci", ['%' + search_query + '%'])
        self.assertEquals(results_list_name[0].first_name, 'first1')

    def tests_search_by_major(self):
        search_query = "major1"
        results_list_major = Profile.objects.raw(
            "SELECT * from matching_profile where major LIKE %s COLLATE utf8_general_ci", ['%' + search_query + '%'])
        self.assertEquals(results_list_major[0].major, 'major1')

    def tests_search_by_courses(self):
        search_query = "course1"
        searched_course = Course.objects.raw(
            "SELECT * from matching_course where course_title LIKE %s COLLATE utf8_general_ci", ['%' + search_query + '%'])
        searched_course_profile_list = []
        for tmp_cs in searched_course:
            for tmp_user in tmp_cs.profile_set.all():
                if tmp_user not in searched_course_profile_list:
                    searched_course_profile_list.append(tmp_user)
        self.assertQuerysetEqual(searched_course_profile_list[0].courses.all(), [
                                 '<Course: course1>'])
