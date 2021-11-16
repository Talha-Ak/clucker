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

    def test_toggle_follow_user(self):
        jane = User.objects.get(username='@janedoe')
        self.assertFalse(self.user.is_following(jane))
        self.assertFalse(jane.is_following(self.user))
        self.user.toggle_follow(jane)
        self.assertTrue(self.user.is_following(jane))
        self.assertFalse(jane.is_following(self.user))
        self.user.toggle_follow(jane)
        self.assertFalse(self.user.is_following(jane))
        self.assertFalse(jane.is_following(self.user))

    def test_follow_counters(self):
        jane = User.objects.get(username='@janedoe')
        petra = User.objects.get(username='@petrapickles')
        peter = User.objects.get(username='@peterpickles')
        self.user.toggle_follow(jane)
        self.user.toggle_follow(petra)
        self.user.toggle_follow(peter)
        jane.toggle_follow(petra)
        jane.toggle_follow(peter)
        self.assertEqual(self.user.follower_count(), 0)
        self.assertEqual(self.user.followee_count(), 3)
        self.assertEqual(jane.follower_count(), 1)
        self.assertEqual(jane.followee_count(), 2)
        self.assertEqual(petra.follower_count(), 2)
        self.assertEqual(petra.followee_count(), 0)
        self.assertEqual(peter.follower_count(), 2)
        self.assertEqual(peter.followee_count(), 0)

    def test_user_cannot_follow_self(self):
        self.user.toggle_follow(self.user)
        self.assertEqual(self.user.follower_count(), 0)
        self.assertEqual(self.user.followee_count(), 0)        

    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except (ValidationError):
            self.fail('Test user is invalid.')

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()
