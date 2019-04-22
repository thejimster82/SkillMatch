from datetime import datetime

from django.test import TestCase, RequestFactory, Client
from .models import Profile, Course, MatchesTable
from django.contrib.auth.models import User
from social_django.models import UserSocialAuth
from .forms import UserForm, ProfileForm
from .views import update_profile, profile, match_exists

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
        buttonBytes = bytearray(buttonString, 'utf-8')
        self.assertTrue(buttonBytes not in response.content)

    def test_year_validation_1(self):
        form_data = {
            'gender':'M',
            'grad_year':2019,
            'bio':'Bio'
        }
        form = ProfileForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_year_validation_2(self):
        super_senior = datetime.now().year + 5
        form_data = {
            'gender':'M',
            'grad_year':super_senior,
            'bio':'Bio'
        }
        form = ProfileForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_year_validation_3(self):
        senior_citizen = 1960
        form_data = {
            'gender':'M',
            'grad_year':senior_citizen,
            'bio':'Bio'
        }
        form = ProfileForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_year_validation_4(self):
        smart_baby = datetime.now().year + 20
        form_data = {
            'gender':'M',
            'grad_year':smart_baby,
            'bio':'Bio'
        }
        form = ProfileForm(data=form_data)
        self.assertFalse(form.is_valid())


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
        self.profile.refresh_from_db()
        response = self.client.get('/home/')
        self.assertTemplateUsed('home.html')


class MatchesTest(TestCase):

    def setUp(self):
        self.u1 = User.objects.create(
            username="b", email="test1@virginia.edu", first_name="first1", last_name="last1")
        self.p1 = Profile.objects.get(user=self.u1)

        self.u2 = User.objects.create(
            username="c", email="test2@virginia.edu", first_name="first2", last_name="last2")
        self.p2 = Profile.objects.get(user=self.u2)

        self.client = Client()

    def test_no_matches(self):
        matches = MatchesTable.objects.filter(from_user=self.u1)
        self.assertFalse(matches.exists())

    def test_match_exists_true(self):
        MatchesTable.objects.create(
            from_user=self.u1, to_user=self.u2, like=True)
        MatchesTable.objects.create(
            from_user=self.u2, to_user=self.u1, like=True)
        is_match = match_exists(self.u1, self.u2)
        self.assertTrue(is_match)

    def test_match_exists_no_like_1(self):
        MatchesTable.objects.create(
            from_user=self.u1, to_user=self.u2, like=False)
        MatchesTable.objects.create(
            from_user=self.u2, to_user=self.u1, like=True)
        is_match = match_exists(self.u1, self.u2)
        self.assertFalse(is_match)

    def test_match_exists_no_like_2(self):
        MatchesTable.objects.create(
            from_user=self.u1, to_user=self.u2, like=True)
        MatchesTable.objects.create(
            from_user=self.u2, to_user=self.u1, like=False)
        is_match = match_exists(self.u1, self.u2)
        self.assertFalse(is_match)

    def test_match_exists_no_like_3(self):
        MatchesTable.objects.create(
            from_user=self.u1, to_user=self.u2, like=False)
        MatchesTable.objects.create(
            from_user=self.u2, to_user=self.u1, like=False)
        is_match = match_exists(self.u1, self.u2)
        self.assertFalse(is_match)

    def test_half_match_1(self):
        MatchesTable.objects.create(
            from_user=self.u1, to_user=self.u2, like=True)
        is_match = match_exists(self.u1, self.u2)
        self.assertFalse(is_match)

    def test_half_match_2(self):
        MatchesTable.objects.create(
            from_user=self.u2, to_user=self.u1, like=True)
        is_match = match_exists(self.u1, self.u2)
        self.assertFalse(is_match)

    def test_post_match_1(self):
        self.client.force_login(self.u2)
        self.client.get('/home/')  # to set first_login = False
        self.client.post('/home/', {
            'r_id': 'b',
            'accept': 'accept'
        })
        self.assertQuerysetEqual(MatchesTable.objects.all(), [
                                 '<MatchesTable: c --> b (True)>'])

    def test_post_match_2(self):
        self.client.force_login(self.u2)
        self.client.get('/home/')  # to set first_login = False
        self.client.post('/home/', {
            'r_id': 'b',
            'reject': 'reject'
        })
        self.assertQuerysetEqual(MatchesTable.objects.all(), [
                                 '<MatchesTable: c --> b (False)>'])


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
            "SELECT * from auth_User where username ILIKE %s", ['%' + search_query + '%'])
        self.assertEquals(results_list[0].username, 'b')

    def test_search_by_first_name(self):
        search_query = "first1"
        results_list_name = Profile.objects.raw(
            "SELECT * from auth_User where first_name ILIKE %s", ['%' + search_query + '%'])

    def tests_search_by_major(self):
        search_query = "major1"
        results_list_major = Profile.objects.raw(
            "SELECT * from matching_profile where major ILIKE %s", ['%' + search_query + '%'])
        self.assertEquals(results_list_major[0].major, 'major1')

    def tests_search_by_courses(self):
        search_query = "course1"
        searched_course = Course.objects.raw(
            "SELECT * from matching_course where course_title ILIKE %s", ['%' + search_query + '%'])
        searched_course_profile_list = []
        for tmp_cs in searched_course:
            for tmp_user in tmp_cs.profile_set.all():
                if tmp_user not in searched_course_profile_list:
                    searched_course_profile_list.append(tmp_user)
        self.assertQuerysetEqual(searched_course_profile_list[0].courses.all(), ['<Course: course1>'])
        
