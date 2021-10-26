from django.test import TestCase
from django.urls import reverse
from microblogs.models import User

class ShowUserViewTestCase(TestCase):
    """Test suite for show_user view"""
    def setUp(self):
        self.user = User.objects.create_user('@johndoe',
            first_name = 'John',
            last_name = 'Doe',
            email='johndoe@example.org',
            bio='I am John Doe.',
            password='Password123',
            is_active=True,
        )
        self.url = reverse('show_user', args=[self.user.id])

    def test_show_user_url(self):
        self.assertEqual(self.url, f'/user/{self.user.id}/')

    def test_get_user(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_user.html')
        user = response.context['user']
        self.assertEqual(user, User.objects.get(id=self.user.id))
