from django.contrib.auth.hashers import check_password
from django.test import TestCase
from django.urls import reverse
from microblogs.forms import PasswordUpdateForm
from microblogs.models import User
from microblogs.tests.helpers import LogInTester, reverse_with_next

class UpdatePasswordViewTestCase(TestCase, LogInTester):
    """Test suite for update_password view"""

    fixtures = ['microblogs/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.url = reverse('update_password')
        self.form_input = {
            'old_password': 'Password123',
            'new_password': 'BetterPassword123',
            'password_confirmation': 'BetterPassword123'
        }

    def test_update_password_url(self):
        self.assertEqual(self.url, '/update_password/')

    def test_get_update_password(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_password.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, PasswordUpdateForm))
        self.assertFalse(form.is_bound)

    def test_get_update_password_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_update_password_fail(self):
        self.client.login(username=self.user.username, password='Password123')
        self.form_input['old_password'] = 'WrongPassword123'
        response = self.client.post(self.url, self.form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_password.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, PasswordUpdateForm))
        self.assertTrue(form.is_bound)
        is_password_correct = check_password(self.form_input['new_password'], self.user.password)
        self.assertFalse(is_password_correct)
        self.assertTrue(self._is_logged_in())

    def test_update_password_success(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.post(self.url, self.form_input, follow=True)
        response_url = reverse('feed')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')
        # Ensure password is correctly hashed.
        self.user = User.objects.get(username='@johndoe')  # R
        is_password_correct = check_password(self.form_input['new_password'], self.user.password)
        self.assertTrue(is_password_correct)
        self.assertTrue(self._is_logged_in())
