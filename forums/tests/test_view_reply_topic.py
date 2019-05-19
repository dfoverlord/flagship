from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from ..forms import PostForm
from ..models import Forum, Post, Topic
from ..views import reply_topic


class ReplyTopicTestCase(TestCase):
    '''
    Base test case to be used in all `reply_topic` view tests
    '''
    def setUp(self):
        self.forum = Forumobjects.create(name='Digital Facets', description='Digital Facets Forum.')
        self.username = 'jack'
        self.password = '123'
        user = User.objects.create_user(username=self.username, email='jack@sparrow.com', password=self.password)
        self.topic = Topic.objects.create(subject='Hello, world', forum=self.forum, starter=user)
        Post.objects.create(message='Lorem ipsum dolor sit amet', topic=self.topic, created_by=user)
        self.url = reverse('reply_topic', kwargs={'pk': self.forum.pk, 'topic_pk': self.topic.pk})


class LoginRequiredReplyTopicTests(ReplyTopicTestCase):
    ''' A test case to verify successful redirection '''
    def test_redirection(self):
        login_url = reverse('login')
        response = self.client.get(self.url)
        self.assertRedirects(response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))


class ReplyTopicTests(ReplyTopicTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.get(self.url)

    ''' A test case to confirm a success status code is returned for a new topic '''
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    ''' A test case to confirm view function is valid '''
    def test_view_function(self):
        view = resolve('/forums/1/topics/1/reply/')
        self.assertEquals(view.func, reply_topic)

    ''' A test case to verify a cross site security token exists '''
    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    ''' A test case to confirm that there is a form '''
    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PostForm)

    '''
      A test case to confirm the view contains the following:
        1. csrf
        2. message textarea
    '''
    def test_form_inputs(self):
        '''
        The view must contain two inputs: csrf, message textarea
        '''
        self.assertContains(self.response, '<input', 1)
        self.assertContains(self.response, '<textarea', 1)
        
        
class SuccessfulReplyTopicTests(ReplyTopicTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {'message': 'hello, world!'})

    ''' A test case to verify successful redirection '''
    def test_redirection(self):
        '''
        A valid form submission should redirect the user
        '''
        url = reverse('topic_posts', kwargs={'pk': self.forum.pk, 'topic_pk': self.topic.pk})
        topic_posts_url = '{url}?page=1#2'.format(url=url)
        self.assertRedirects(self.response, topic_posts_url)

    ''' A test case to validate a created reply '''
    def test_reply_created(self):
        '''
        The total post count should be 2
        The one created in the `ReplyTopicTestCase` setUp
        and another created by the post data in this class
        '''
        self.assertEquals(Post.objects.count(), 2)
        
        
class InvalidReplyTopicTests(ReplyTopicTestCase):
    def setUp(self):
        '''
        Submit an empty dictionary to the `reply_topic` view
        '''
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.response = self.client.post(self.url, {})

    ''' A test case to confirm an invalid form submission should return to the same page '''
    def test_status_code(self):
        '''
        An invalid form submission should return to the same page
        '''
        self.assertEquals(self.response.status_code, 200)

    ''' A test case to validate form errors '''
    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)