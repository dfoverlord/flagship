from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from ..forms import NewTopicForm
from ..models import Forum, Post, Topic
from ..views import new_topic


class NewTopicTests(TestCase):
    def setUp(self):
        Forum.objects.create(name='Digital Facets', description='Digital Facets Forum.')
        User.objects.create_user(username='jack', email='jack@sparrow.com', password='123')
        self.client.login(username='jack', password='123')

    ''' A test case to confirm a success status code is returned for a new topic '''
    def test_new_topic_view_success_status_code(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    ''' A test case to verify new topic does not return a 404 response (Page Not Found) '''
    def test_new_topic_view_not_found_status_code(self):
        url = reverse('new_topic', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    ''' A test case to confirm new topic url resolves to new topic view '''
    def test_new_topic_url_resolves_new_topic_view(self):
        view = resolve('/forums/1/new/')
        self.assertEquals(view.func, new_topic)

    ''' A test case to confirm new topic contains a link back to forum topics '''
    def test_new_topic_view_contains_link_back_to_forum_topics_view(self):
        new_topic_url = reverse('new_topic', kwargs={'pk': 1})
        forum_topics_url = reverse('forum_topics', kwargs={'pk': 1})
        response = self.client.get(new_topic_url)
        self.assertContains(response, 'href="{0}"'.format(forum_topics_url))

    ''' A test case to verify a cross site security token exists '''
    def test_csrf(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    ''' A test case to confirm that there is a form '''
    def test_contains_form(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        form = response.context.get('form')
        self.assertIsInstance(form, NewTopicForm)

    ''' A test case to validate that new topic post data is valid '''
    def test_new_topic_valid_post_data(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        data = {
            'subject': 'Test title',
            'message': 'Lorem ipsum dolor sit amet'
        }
        self.client.post(url, data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())

    ''' A test case to verify if new topic post data is invalid '''
    def test_new_topic_invalid_post_data(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.post(url, {})
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    ''' A test case to verify if new topic is invalid and contains empty fields '''
    def test_new_topic_invalid_post_data_empty_fields(self):
        '''
        Invalid post data should not redirect
        The expected behavior is to show the form again with validation errors
        '''
        url = reverse('new_topic', kwargs={'pk': 1})
        data = {
            'subject': '',
            'message': ''
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())


class LoginRequiredNewTopicTests(TestCase):
    def setUp(self):
        Forum.objects.create(name='Digital Facets', description='Digital Facets Forum.')
        self.url = reverse('new_topic', kwargs={'pk': 1})
        self.response = self.client.get(self.url)

    ''' A test case to verify successful redirection '''
    def test_redirection(self):
        login_url = reverse('login')
        self.assertRedirects(self.response, '{login_url}?next={url}'.format(login_url=login_url, url=self.url))
