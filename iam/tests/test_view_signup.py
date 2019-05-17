from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from ..forms import SignUpForm
from ..views import signup
from django.contrib.auth.forms import UsernameField

class SignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)
     
    ''' A test case to check for a return status code of '200' '''   
    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    
    ''' A test case to verify the url resolves to a signup view '''
    def test_signup_url_resolves_signup_view(self):
        view = resolve('/signup/')
        self.assertEquals(view.func, signup)
    
    ''' A test case to check for cross site security token '''
    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')
    
    ''' A test case to confirm there is a form present '''
    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignUpForm)
    
    ''' A test case to validate inputs '''
    '''
        This view MUST contain five inputs
          1.  csrf
          2.  username
          3.  email
          4.  password1
          5.  password2 (this is the verification password)
        '''
    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 5)
        ''' 1 text field '''
        self.assertContains(self.response, 'type="text"', 1)
        ''' 1 email address '''
        self.assertContains(self.response, 'type="email"', 1)
        ''' 2 password fields '''
        self.assertContains(self.response, 'type="password"', 2)
        
        
        
class SuccessfulSignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        data = {
            'username': 'jack',
            'email': 'jack@sparrow.com',
            'password1': 'C4@n63Th!sP@55w0rdN0w',
            'password2': 'C4@n63Th!sP@55w0rdN0w',
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('home')
    
    ''' A test case to check that user is redirected to home page after a valid form submission '''
    def test_redirection(self):
        self.assertRedirects(self.response, self.home_url)
        
    ''' A test case to confirm whether a user exists '''
    def test_user_creation(self):
        self.assertTrue(User.objects.exists())
        
    ''' A test case to create a new request to an arbitrary page.  The resulting response show now '''
    ''' have a 'user' in its context, after a successful signup '''    
    def test_user_authentication(self):
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)
        

class InvalidSignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.post(url, {})  # submit an empty dictionary
        
    ''' A test case to confirm that an invalid form submission should return to the same page '''
    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    
    ''' A test case to check form errors '''
    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
    
    ''' A test case to confirm a user is not created b/c it already exists '''
    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())