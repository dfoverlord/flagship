from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from django.urls import reverse

class PasswordResetMailTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='jack', email='jack@sparrow.com', password='C4@n63Th!sP@55w0rdN0w')
        self.response = self.client.post(reverse('password_reset'), {'email': 'jack@sparrow.com'})
        self.email = mail.outbox[0]
        
    ''' A test case to validate email subject '''
    def test_email_subject(self):
        self.assertEqual('[Digital Facets] Please reset your password', self.email.subject)
        
    ''' A test case to validate email body '''
    def test_email_body(self):
        context = self.response.context
        token = context.get('token')
        uid = context.get('uid')
        password_reset_token_url = reverse('password_reset_confirm', kwargs={
            'uidb64': uid,
            'token': token
        })
        self.assertIn(password_reset_token_url, self.email.body)
        self.assertIn('jack', self.email.body)
        self.assertIn('jack@sparrow.com', self.email.body)
        
    ''' A test case to validate email to '''
    def test_email_to(self):
        self.assertEqual(['jack@sparrow.com', ], self.email.to)