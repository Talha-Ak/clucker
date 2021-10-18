from django.test import TestCase
from django.urls import reverse
from microblogs.models import User

class UserListViewTestCase(TestCase):

    def setUp(self):
        self.url = reverse('user_list')

    def test_log_out_url(self):
        self.assertEqual(self.url, '/users/')

    def test_get_user_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_list.html')
        user_list = response.context['users']
        self.assertEqual(list(user_list), list(User.objects.all()))