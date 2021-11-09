"""Tests of the feed view."""
from django.test import TestCase
from django.urls import reverse
from microblogs.forms import PostForm
from microblogs.models import User
from microblogs.tests.helpers import reverse_with_next, create_posts

class FeedViewTestCase(TestCase):
    """Tests of the feed view."""

    fixtures = [
        'microblogs/tests/fixtures/default_user.json',
        'microblogs/tests/fixtures/other_users.json',
    ]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.url = reverse('feed')

    def test_feed_url(self):
        self.assertEqual(self.url,'/feed/')

    def test_get_feed(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feed.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, PostForm))
        self.assertFalse(form.is_bound)

    def test_get_feed_redirect_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_feed_shows_self_posts(self):
        self.client.login(username=self.user.username, password='Password123')
        other_user = User.objects.get(username='@janedoe')
        create_posts(other_user, 100, 103)
        create_posts(self.user, 200, 203)
        response = self.client.get(self.url)
        for count in range(100, 103):
            self.assertNotContains(response, f"Post__{count}")
        for count in range(200, 203):
            self.assertContains(response, f"Post__{count}")
