from django.test import TestCase
from django.urls import reverse
from microblogs.models import User
from microblogs.tests.helpers import reverse_with_next

class UserListViewTestCase(TestCase):
    """Test suite for user_list view"""

    fixtures = ['microblogs/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('user_list')
        self.user = User.objects.get(username='@johndoe')

    def test_user_list_url(self):
        self.assertEqual(self.url, '/users/')

    def test_get_user_list(self):
        self.client.login(username='@johndoe', password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_list.html')
        user_list = response.context['users']
        self.assertEqual(list(user_list), list(User.objects.filter(is_superuser=False)))

    def test_get_user_list_redirect_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
