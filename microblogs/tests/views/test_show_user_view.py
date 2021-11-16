from django.test import TestCase
from django.urls import reverse
from microblogs.models import User, Post
from microblogs.tests.helpers import reverse_with_next, create_posts

class ShowUserViewTestCase(TestCase):
    """Test suite for show_user view"""

    fixtures = [
        'microblogs/tests/fixtures/default_user.json',
        'microblogs/tests/fixtures/other_users.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.target_user = User.objects.get(username='@janedoe')
        self.url = reverse('show_user', kwargs={'user_id': self.target_user.id})

    def test_show_user_url(self):
        self.assertEqual(self.url, f'/user/{self.target_user.id}/')

    def test_get_user(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_user.html')
        user = response.context['user']
        self.assertEqual(user, User.objects.get(id=self.target_user.id))

    def test_get_user_with_valid_id(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_user.html')
        self.assertContains(response, 'Jane Doe')
        self.assertContains(response, '@janedoe')
        followable = response.context['followable']
        self.assertTrue(followable)

    def test_get_user_with_own_id(self):
        self.client.login(username=self.user.username, password='Password123')
        url = reverse('show_user', kwargs={'user_id': self.user.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'show_user.html')
        self.assertContains(response, 'John Doe')
        self.assertContains(response, '@johndoe')
        followable = response.context['followable']
        self.assertFalse(followable)

    def test_get_user_with_invalid_id(self):
        self.client.login(username=self.user.username, password='Password123')
        url = reverse('show_user', args=[self.user.id + 9999])
        response = self.client.get(url, follow=True)
        response_url = reverse('user_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'user_list.html')

    def test_get_user_redirect_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_show_user_displays_only_their_posts(self):
        self.client.login(username=self.user.username, password='Password123')
        other_user = User.objects.get(username='@janedoe')
        create_posts(other_user, 100, 103)
        create_posts(self.user, 200, 203)
        url = reverse('show_user', kwargs={'user_id': other_user.id})
        response = self.client.get(url)
        for count in range(100, 103):
            self.assertContains(response, f"Post__{count}")
        for count in range(200, 203):
            self.assertNotContains(response, f"Post__{count}")
