from django.forms import ModelForm

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from ..models import Forum, Post, Topic
from ..views import PostUpdateView


''' A base test case to be used in all PostUpdateView view tests '''
class PostUpdateViewTestCase(TestCase):
    def setUp(self):
        self.forum = Forum.objects.create(name='Digital Facets', description='Digital Facets Forum.')
        self.username = 'jack'
        self.password = '123'
        user = User.objects.create_user(username=self.username, email='jack@sparrow.com', password=self.password)
        self.topic = Topic.objects.create(subject='Hello, world', forum=self.forum, creator=user)
        self.post = Post.objects.create(message='Lorem ipsum dolor sit amet', topic=self.topic, created_by=user)
        self.url = reverse('edit_post', kwargs={
            'pk': self.forum.pk,
            'topic_pk': self.topic.pk,
            'post_pk': self.post.pk
        })
        
        
''' A test case to verify only logged in users can edit the posts '''    
class LoginRequiredPostUpdateViewTests(PostUpdateViewTestCase):
    def test_redirection(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))
        
        
''' Create a new user different from the one who posted ''' 
class UnauthorizedPostUpdateViewTests(PostUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        username = 'jane'
        password = '321'
        user = User.objects.create_user(username=username, email='jane@calamity.com', password=password)
        self.client.login(username=username, password=password)
        self.response = self.client.get(self.url)
        
    ''' A test case to verify that a topic should only be edited by the owner. Unauthorized users should get a 404 response (Page Not Found) '''
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 404)
        
        
class PostUpdateViewTests(PostUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)
        
    ''' A test case to validate status code is "200" '''
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)
        
    ''' A test case to verify  view class '''   
    def test_view_class(self):
        view = resolve('/forums/1/topics/1/posts/1/edit/')
        self.assertEquals(view.func.view_class, PostUpdateView)
        
    ''' A test case to verify a cross site security token exists '''
    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')
        
    ''' A test case to confirm that there is a form '''
    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, ModelForm)
        
    '''
      A test case to confirm the view contains the following:
        1. csrf
        2. message textarea
    '''  
    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 1)
        self.assertContains(self.response, '<textarea', 1)
        
        
class SuccessfulPostUpdateViewTests(PostUpdateViewTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {'message': 'edited message'})
        
    ''' A test case to validate redirection '''  
    def test_redirection(self):
        topic_posts_url = reverse('topic_posts', kwargs={'pk': self.forum.pk, 'topic_pk': self.topic.pk})
        self.assertRedirects(self.response, topic_posts_url)
        
    ''' A test case to test post changed '''
    def test_post_changed(self):
        self.post.refresh_from_db()
        self.assertEquals(self.post.message, 'edited message')
        
        
class InvalidPostUpdateViewTests(PostUpdateViewTestCase):
    ''' Submit an empty dictionary to the 'reply_topic' view '''
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {})
        
    ''' A test case to confirm that an invalid form submission should return to the same page '''
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)
        
    ''' A test case to validate form errors '''
    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)