from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

class PasswordChangeTests(TestCase):
    def setUp(self):
        username = 'jack'
        password = 'C4@n63Th!sP@55w0rdN0w'
        User.objects.create_user(username=username, email='jack@sparrow.com', password=password)
        url = reverse('pages:password_change')
        self.client.login(username=username, password=password)
        self.response = self.client.get(url)
        
    ''' A test case to validate status code is "200" '''
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)
        
    ''' A test case to verify url resolves to correct view '''
    def test_url_resolves_correct_view(self):
        view = resolve('/settings/password/')
        self.assertEquals(view.func.view_class, auth_views.PasswordChangeView)
        
    ''' A test case to verify a cross site security token exists '''
    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')
        
    ''' A test case to confirm that there is a form '''
    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordChangeForm)
        
    '''
      A test case to confirm the view contains the following:
        1. csrf
        2. email
    '''
    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 4)
        self.assertContains(self.response, 'type="password"', 3)
        
    
class LoginRequiredPasswordChangeTests(TestCase):
    ''' A test case to verify redirection '''
    def test_redirection(self):
        url = reverse('pages:password_change')
        login_url = reverse('pages:login')
        response = self.client.get(url)
        self.assertRedirects(response, f'{login_url}?next={url}')
        

class PasswordChangeTestCase(TestCase):
    ''' 
    A base test case for form processing
    accepts a 'data' dict to POST to the view
    '''
    def setUp(self, data={}):
        self.user = User.objects.create_user(username='jack', email='jack@sparrow.com', password='old_password')
        self.url = reverse('pages:password_change')
        self.client.login(username='jack', password='old_password')
        self.response = self.client.post(self.url, data)
        
        
class SuccessfulPasswordChangeTests(PasswordChangeTestCase):
    def setUp(self):
        super().setUp({
            'old_password': 'old_password',
            'new_password1': 'new_password',
            'new_password2': 'new_password',
        })
        
    ''' A test case to verify redirection. A valid form submission should redirect the user '''
    def test_redirection(self):
        self.assertRedirects(self.response, reverse('password_change_done'))
        
    '''
    refresh the user instance from database to get the new password
    hash updated by the change password view.
    '''
    def test_password_changed(self):
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('new_password'))
        
    '''
    Create a new request to an arbitrary page.
    The resulting response should now have an `user` to its context, after a successful sign up.
    '''
    def test_user_authentication(self):
        response = self.client.get(reverse('home'))
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)
        
        
class InvalidPasswordChangeTests(PasswordChangeTestCase):
    def test_status_code(self):
        '''
        An invalid form submission should return to the same page
        '''
        self.assertEquals(self.response.status_code, 200)
        
    ''' A test case to test form errors '''
    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
        
    ''' A test case to confirm password does not get reset '''
    def test_didnt_change_password(self):
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('old_password'))