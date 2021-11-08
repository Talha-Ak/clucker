from django.test import TestCase
from django.urls import reverse
from microblogs.forms import PostForm
from microblogs.models import User, Post

class NewPostViewTestCase(TestCase):
    """Test suite for new_post view"""

    fixtures = ['microblogs/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('new_post')
        self.user = User.objects.get(username='@johndoe')
        self.post = {
            'text': 'This is just some example text to test things out.',
        }

    def test_new_post_url(self):
        self.assertEqual(self.url, '/new_post/')

    def test_valid_post_logged_in_saved(self):
        self.client.login(username='@johndoe', password='Password123')
        before_count = Post.objects.count()
        response = self.client.post(self.url, self.post, follow=True)
        after_count = Post.objects.count()
        self.assertEqual(after_count, before_count + 1)
        saved_post = Post.objects.filter(author=self.user)[0]
        self.assertEqual(saved_post.text, self.post['text'])
        response_url = reverse('feed')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')

    def test_valid_post_but_not_logged_in(self):
        before_count = Post.objects.count()
        response = self.client.post(self.url, self.post, follow=True)
        after_count = Post.objects.count()
        self.assertEqual(after_count, before_count)

    def test_invalid_post_logged_in(self):
        self.post['text'] = 'x' * 281
        self.client.login(username='@johndoe', password='Password123')
        before_count = Post.objects.count()
        response = self.client.post(self.url, self.post, follow=True)
        after_count = Post.objects.count()
        self.assertEqual(after_count, before_count)
        response_url = reverse('feed')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')
