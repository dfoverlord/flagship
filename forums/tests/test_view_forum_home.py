from django.test import TestCase
from django.urls import resolve, reverse

from ..models import Forum
from ..views import FormListView

class ForumHomeTests(TestCase):
    def setUp(self):
        self.forum = Forum.objects.create(name='Digital Facets', description='Digital Facets Forums.')
        url = reverse('home')
        self.response = self.client.get(url)
        
    ''' A test case to validate status code is "200" '''
    def test_forum_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)
        
    ''' A test case to confirm forum home url resolves to home view '''
    def test_forum_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func.view_class, ForumListView)
        
    ''' A test case to validate forum home view contains links to topics page '''
    def test_forum)home_view_contains_link_to_topics_page(self):
        forum_topics_url = reverse('forum_topics', kwargs={'pk': self.forum.pk})
        self.assertContains(self.response, 'href="{0}"'.format(forum_topics_url))