from django.core.exceptions import ValidationError
from django.test import TestCase
from microblogs.models import User, Post

class PostModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='@johndoe',
            first_name='John',
            last_name='Doe',
            email='johndoe@example.org',
            password='Password123',
            bio='This is a test bio.'
        )
        self.post = Post.objects.create(
            author=self.user,
            text='This is just some example text to test things out.',
        )

    def test_valid_post(self):
        self._assert_post_is_valid()

    def test_post_text_280_chars_valid(self):
        self.post.text = 'x' * 280
        self._assert_post_is_valid()

    def test_post_text_281_chars_invalid(self):
        self.post.text = 'x' * 281
        self._assert_post_is_invalid()

    def _assert_post_is_valid(self):
        try:
            self.post.full_clean()
        except (ValidationError):
            self.fail('Test user is invalid.')

    def _assert_post_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.post.full_clean()
