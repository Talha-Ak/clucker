from django.contrib.auth.hashers import check_password
from django.test import TestCase
from django import forms
from microblogs.forms import PasswordUpdateForm
from microblogs.models import User

class SignUpFormTestCase(TestCase):
    """Test suite for PasswordUpdateForm"""

    fixtures = ['microblogs/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.form_input = {
            'old_password': 'Password123',
            'new_password': 'BetterPassword123',
            'password_confirmation': 'BetterPassword123'
        }

    def test_valid_password_update_form(self):
        form = PasswordUpdateForm(self.user, data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = PasswordUpdateForm(self.user)
        self.assertIn('old_password', form.fields)
        old_password_widget = form.fields['old_password'].widget
        self.assertTrue(isinstance(old_password_widget, forms.PasswordInput))
        self.assertIn('new_password', form.fields)
        new_password_widget = form.fields['new_password'].widget
        self.assertTrue(isinstance(new_password_widget, forms.PasswordInput))
        self.assertIn('password_confirmation', form.fields)
        password_confirmation_widget = form.fields['password_confirmation'].widget
        self.assertTrue(isinstance(password_confirmation_widget, forms.PasswordInput))

    def test_old_password_must_match(self):
        self.form_input['old_password'] = 'WrongPassword123'
        form = PasswordUpdateForm(self.user, data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_uppercase(self):
        self.form_input['new_password'] = 'password123'
        self.form_input['password_confirmation'] = 'password123'
        form = PasswordUpdateForm(self.user, data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_lowercase(self):
        self.form_input['new_password'] = 'PASSWORD123'
        self.form_input['password_confirmation'] = 'PASSWORD123'
        form = PasswordUpdateForm(self.user, data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_number(self):
        self.form_input['new_password'] = 'Password'
        self.form_input['password_confirmation'] = 'Password'
        form = PasswordUpdateForm(self.user, data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_conf_must_be_identical(self):
        self.form_input['password_confirmation'] = 'Otherpassword123'
        form = PasswordUpdateForm(self.user, data=self.form_input)
        self.assertFalse(form.is_valid())
