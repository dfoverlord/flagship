from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from ..models import Forum, Post, Topic
from ..views import PostListView


class TopicPostsTests(TestCase):
    def setUp(self):
        forum = Forum.objects.create(name='Digital Facets', description='Digital Facets Forum.')
        user = User.objects.create_user(username='jack', email='jack@sparrow.com', password='123')
        topic = Topic.objects.create(subject='Hello, world', forum=forum, creator=user)
        Post.objects.create(message='Lorem ipsum dolor sit amet', topic=topic, created_by=user)
        url = reverse('topic_posts', kwargs={'pk': forum.pk, 'topic_pk': topic.pk})
        self.response = self.client.get(url)

    ''' A test case to confirm a success status code is returned for a topic post '''
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    ''' A test case to confirm view function is valid '''
    def test_view_function(self):
        view = resolve('/forums/1/topics/1/')
        self.assertEquals(view.func.view_class, PostListView)