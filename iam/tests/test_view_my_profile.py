from django.forms import ModelForm
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from ..views import UserUpdateView

class MyProfileTestCase(TestCase):
    def setUp(self):
        self.username = 'jack'
        self.password = 'C4@n63Th!sP@55w0rdN0w'
        self.user = User.objects.create_user(username=self.username, email='jack@sparrow.com', password=self.password)
        self.url = reverse('my_profile')
        
        
class MyProfileTests(MyProfileTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)
        
    ''' A test case to validate status code is "200" '''
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)
        
    ''' A test case to confirm the url resolves to the correct view '''
    def test_url_resolves_correct_view(self):
        view = resolve('/settings/profile/')
        self.assertEquals(view.func.view_class, UserUpdateView)
        
    ''' A test case to verify a cross site security token exists '''
    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')
        
    ''' A test case to confirm that there is a form '''
    def test_contains_form(self):
        form = self.response.context['form']
        self.assertIsInstance(form, ModelForm)
        
    '''
      A test case to confirm the view contains the following:
        1. csrf
        2. first_name
        3. last_name
        4. email
    '''
    def test_form_inputs(self):
       self.assertContains(self.response, '<input', 4)
       self.assertContains(self.response, 'type="text"', 2)
       self.assertContains(self.response, 'type="email"', 1) 
       

class LoginRequiredMyProfileTests(TestCase):
    def test_redirection(self):
        url = reverse('my_profile')
        login_url = reverse('login')
        response = self.client.get(url)
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=url))


class SuccessfulMyProfileTests(MyProfileTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {
            'first_name': 'Jack',
            'last_name': 'Sparrow',
            'email': 'jacksparrow@example.com',
        })
    
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
        
    ''' A test case to test form errors '''
    def test_form_errors(self):
        form = self.response.context['form']
        self.assertTrue(form.errors)