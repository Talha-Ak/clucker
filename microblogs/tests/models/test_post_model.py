from django.core.exceptions import ValidationError
from django.test import TestCase
from microblogs.models import User, Post

class PostModelTestCase(TestCase):
    """Test suite for the Post model"""

    fixtures = ['microblogs/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
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
