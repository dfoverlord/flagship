from django.test import TestCase
from django.urls import resolve, reverse

class HomeTests(TestCase):
    def setUp(self):
        url = reverse('pages:home')
        self.response = self.client.get(url)

    ''' A test case to verify that response code is "200" '''
    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)