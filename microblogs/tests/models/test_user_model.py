from django.core.exceptions import ValidationError
from django.test import TestCase
from microblogs.models import User

class UserModelTestCase(TestCase):
    """Test suite for the User model."""

    fixtures = ['microblogs/tests/fixtures/default_user.json',
                'microblogs/tests/fixtures/other_users.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')

    def test_valid_user(self):
        self._assert_user_is_valid()

    def test_username_not_blank(self):
        self.user.username = ''
        self._assert_user_is_invalid()

    def test_username_30_chars_valid(self):
        self.user.username = '@' + 'x' * 29
        self._assert_user_is_valid()

    def test_username_31_chars_invalid(self):
        self.user.username = '@' + 'x' * 30
        self._assert_user_is_invalid()

    def test_username_unique(self):
        User.objects.get(username='@janedoe')

        self.user.username = '@janedoe'
        self._assert_user_is_invalid()

    def test_username_start_with_atsign(self):
        self.user.username = 'johndoe' # No @
        self._assert_user_is_invalid()

    def test_username_contains_only_alphanumerical_after_atsign(self):
        self.user.username = '@john!doe'
        self._assert_user_is_invalid()

    def test_username_contains_minimum_3_characters(self):
        self.user.username = '@me'
        self._assert_user_is_invalid()

    def test_username_allowed_numbers(self):
        self.user.username = '@j0hndoe2'
        self._assert_user_is_valid()

    def test_username_only_one_atsign(self):
        self.user.username = '@@j0hndoe2'
        self._assert_user_is_invalid()

    def test_first_name_not_blank(self):
        self.user.first_name = ''
        self._assert_user_is_invalid()

    def test_first_name_50_chars_valid(self):
        self.user.first_name = 'x' * 50
        self._assert_user_is_valid()

    def test_first_name_51_chars_invalid(self):
        self.user.first_name = 'x' * 51
        self._assert_user_is_invalid()

    def test_last_name_not_blank(self):
        self.user.last_name = ''
        self._assert_user_is_invalid()

    def test_last_name_50_chars_valid(self):
        self.user.last_name = 'x' * 50
        self._assert_user_is_valid()

    def test_last_name_51_chars_invalid(self):
        self.user.last_name = 'x' * 51
        self._assert_user_is_invalid()

    def test_email_unique(self):
        User.objects.get(username='@janedoe')
        self.user.email = 'janedoe@example.org'
        self._assert_user_is_invalid()

    def test_bio_blank_valid(self):
        self.user.bio = ''
        self._assert_user_is_valid()

    def test_bio_520_chars_valid(self):
        self.user.bio = 'x' * 520
        self._assert_user_is_valid()

    def test_bio_521_chars_invalid(self):
        self.user.bio = 'x' * 521
        self._assert_user_is_invalid()

    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except (ValidationError):
            self.fail('Test user is invalid.')

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()
