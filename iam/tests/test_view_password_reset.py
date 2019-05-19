from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.test import TestCase
from django.urls import resolve, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


class PasswordResetTests(TestCase):
    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.get(url)
    
    ''' A test case to validate status code is "200" '''
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    ''' A test case to check for a valid view '''
    def test_view_function(self):
        view = resolve('/reset/')
        self.assertEquals(view.func.view_class, auth_views.PasswordResetView)
    
    ''' A test case to verify a cross site security token exists '''
    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')
        
    ''' A test case to confirm that there is a form '''
    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordResetForm)
        
    ''' 
      A test case to confirm the view contains the following:
        1. csrf
        2. email
    '''
    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 2)
        self.assertContains(self.response, 'type="email"', 1)
        

class SuccessfulPasswordResetTests(TestCase):
    def setUp(self):
        email = 'jack@sparrow.com'
        User.objects.create_user(username='jack', email=email, password='C4@n63Th!sP@55w0rdN0w')
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email': email})
    
    ''' A test case to verify correct redirection '''
    def test_redirection(self):
        url = reverse('password_reset_done')
        self.assertRedirects(self.response, url)
        
    ''' A test case to confirm password reset email was sent '''
    def test_send_password_reset_email(self):
        self.assertEqual(1, len(mail.outbox))
        
    
class InvalidPasswordResetTests(TestCase):
    def setUp(self):
        url = reverse('password_reset')
        self.response = self.client.post(url, {'email': 'donotexist@email.com'})
        
    ''' A test case to verify correct redirection '''
    def test_redirection(self):
        url = reverse('password_reset_done')
        self.assertRedirects(self.response, url)
        
    ''' A test case to confirm no reset email is sent '''
    def test_no_reset_email_sent(self):
        self.assertEqual(0, len(mail.outbox))
        

class PasswordResetDoneTests(TestCase):
    def setUp(self):
        url = reverse('password_reset_done')
        self.response = self.client.get(url)
        
    ''' A test case to verify status code is "200" '''
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)
        
    ''' A test case to check for a valid view '''
    def test_view_function(self):
        view = resolve('/reset/done/')
        self.assertEquals(view.func.view_class, auth_views.PasswordResetDoneView)
        
        
class PasswordResetConfirmTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='jack', email='jack@sparrow.com', password='C4@n63Th!sP@55w0rdN0w')
        '''
          create a valid password reset token
          based on how django creates the token internally:
          https://github.com/django/django/blob/1.11.5/django/contrib/auth/forms.py#L280
        '''
        ''' self.uid = urlsafe_base64_encode(force_bytes(user.pk)).decode() '''
        self.uid = urlsafe_base64_encode(force_bytes(user.pk))
        self.token = default_token_generator.make_token(user)
        
        url = reverse('password_reset_confirm', kwargs={'uidb64': self.uid, 'token': self.token})
        self.response = self.client.get(url, follow=True)
        
    ''' A test case to verify status code is "200" '''
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)
        
    ''' A test case to check for a valid view '''
    def test_view_function(self):
        view = resolve('/reset/{uidb64}/{token}/'.format(uidb64=self.uid, token=self.token))
        self.assertEquals(view.func.view_class, auth_views.PasswordResetConfirmView)
        
    ''' A test case to verify a cross site security token exists '''
    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')
        
    ''' A test case to confirm that there is a form '''
    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SetPasswordForm)
        
    ''' 
      A test case to confirm the view contains the following:
        1. csrf
        2. email
    '''
    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 3)
        self.assertContains(self.response, 'type="password"', 2)
        
    
class InvalidPasswordResetConfirmTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='jack', email='jack@sparrow.com', password='123abc')
        ''' uid = urlsafe_base64_encode(force_bytes(user.pk)).decode() '''
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        
        '''
        invalidate the token by changing the password
        '''
        user.set_password('abc123')
        user.save()
        
        url = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        self.response = self.client.get(url)
        
    ''' A test case to verify status code is "200" '''
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)
        
    ''' A test case to validate html '''
    def test_html(self):
        password_reset_url = reverse('password_reset')
        self.assertContains(self.response, 'invalid password reset link')
        self.assertContains(self.response, 'href="{0}"'.format(password_reset_url))
    
    
class PasswordResetCompleteTests(TestCase):
    def setUp(self):
        url = reverse('password_reset_complete')
        self.response = self.client.get(url)
        
    ''' A test case to verify status code is "200" '''
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)
        
    ''' A test case to check for a valid view '''
    def test_view_function(self):
        view = resolve('/reset/complete/')
        self.assertEquals(view.func.view_class, auth_views.PasswordResetCompleteView)