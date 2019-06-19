from django.forms import ModelForm
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve, reverse
from PIL import Image

from ..models import Profile
from ..forms import SignUpForm, UserInformationUpdateForm, ProfileForm
from ..views import update_profile
from ..signals import create_or_update_user_profile

class MyProfileTestCase(TestCase):
    def setUp(self):
        self.username = 'jack'
        self.password = '123abc'
        User = get_user_model()
        self.user = User.objects.create_user(username=self.username, email='jack@sparrow.com', password=self.password)
        self.url = reverse('pages:my_profile')
        
        
class MyProfileTests(MyProfileTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)
        
    ''' A test case to verify a profile is created when new user is added '''
    def test_profile_creation(self):
        self.assertIsInstance(self.user.profile, Profile)
        '''
        call the save method of the user to activate the signal again, and check that it doesn't
        try to create another profile instance
        '''
        self.user.save()
        self.assertIsInstance(self.user.profile, Profile)   
        
    ''' A test case to validate status code is "200" '''
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)
        
    ''' A test case to confirm the url resolves to the correct view '''
    def test_url_resolves_correct_view(self):
        view = resolve('/settings/profile/')
        self.assertEquals(view.func, update_profile)
        
    ''' A test case to verify a cross site security token exists '''
    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')
        
    ''' A test case to confirm that there is a user_form '''
    def test_contains_user_form(self):
        user_form = self.response.context['user_form']
        self.assertIsInstance(user_form, ModelForm)
        
    ''' A test case to confirm that there is a profile_form '''
    def test_contains_profile_form(self):
        profile_form = self.response.context['profile_form']
        self.assertIsInstance(profile_form, ModelForm)
        
    '''
      A test case to confirm the view contains the following:
        1. csrf
        2. first_name
        3. last_name
        4. email
        5. company
        6. website
        7. short_bio
        8. imagefield
    '''
    def test_form_inputs(self):
       self.assertContains(self.response, '<input', 8)
       self.assertContains(self.response, 'type="text"', 5)
       self.assertContains(self.response, 'type="email"', 1)
       

class LoginRequiredMyProfileTests(TestCase):
    ''' A test case to validate redirection '''
    def test_redirection(self):
        url = reverse('pages:my_profile')
        login_url = reverse('pages:login')
        response = self.client.get(url)
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=url))


class SuccessfulMyProfileTests(MyProfileTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        
        self.response = self.client.post(self.url, {
            'first_name': 'Jack', 'last_name': 'Sparrow', 'email': 'jacksparrow@example.com',  
            'user.profile.company': 'Acme', 'user.profile.website': 'acme.com', 'user.profile.short_bio': 'About Me',
        })
        
        '''
        self.response = self.client.post(self.url, {
            'first_name': 'Jack',
            'last_name': 'Sparrow',
            'email': 'jacksparrow@example.com',
        })
        '''
    
    ''' A test case to verify form redirection on successful submission '''
    def test_redirection(self):
        self.assertRedirects(self.response, self.url)
        
    ''' A test case to verify a data change '''
    def test_data_changed(self):
        self.user.refresh_from_db()
        self.assertEquals('Jack', self.user.first_name)
        self.assertEquals('Sparrow', self.user.last_name)
        self.assertEquals('jacksparrow@example.com', self.user.email)
        
        
class InvalidMyProfileTests(MyProfileTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {
            'first_name': 'longstring' * 100
        })
        
    ''' A test case to validate status code is "200" '''
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)
        
    ''' A test case to test user_form errors '''
    def test_user_form_errors(self):
        user_form = self.response.context['user_form']
        self.assertTrue(user_form.errors)
        
    ''' A test case to test profile_form errors '''
    def test_profile_form_errors(self):
        profile_form = self.response.context['profile_form']
        self.assertTrue(profile_form.errors)