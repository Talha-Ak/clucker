from django.test import TestCase
from django.urls import reverse
from microblogs.models import User

class ShowUserViewTestCase(TestCase):
    """Test suite for show_user view"""

    fixtures = ['microblogs/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.url = reverse('show_user', kwargs={'user_id': self.user.id})

    def test_show_user_url(self):
        self.assertEqual(self.url, f'/user/{self.user.id}/')

    def test_get_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_user.html')
        user = response.context['user']
        self.assertEqual(user, User.objects.get(id=self.user.id))

    def test_get_user_with_invalid_id(self):
        self.client.login(username=self.user.username, password='Password123')
        url = reverse('show_user', args=[self.user.id + 1])
        response = self.client.get(url, follow=True)
        response_url = reverse('user_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'user_list.html')
