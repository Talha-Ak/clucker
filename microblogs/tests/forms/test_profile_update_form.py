from django.test import TestCase
from django import forms
from microblogs.forms import ProfileUpdateForm
from microblogs.models import User

class ProfileUpdateFormTestCase(TestCase):
    """Test suite for ProfileUpdateForm"""

    fixtures = ['microblogs/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.form_input = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@otherdomain.com',
            'bio': 'Hello, this is my new bio.',
        }

    def test_valid_update_form(self):
        form = ProfileUpdateForm(data=self.form_input, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_update_form_has_necessary_fields(self):
        form = ProfileUpdateForm(instance=self.user)
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('email', form.fields)
        email_field = form.fields['email']
        self.assertTrue(isinstance(email_field, forms.EmailField))
        self.assertIn('bio', form.fields)

    def test_update_form_uses_model_validation(self):
        self.form_input['email'] = 'bad$@email@test'
        form = ProfileUpdateForm(data=self.form_input, instance=self.user)
        self.assertFalse(form.is_valid())

    def test_update_form_correct_save(self):
        form = ProfileUpdateForm(data=self.form_input, instance=self.user)
        self.assertTrue(form.has_changed())
        self.assertEqual(form.changed_data, ['email', 'bio'])
        before_count = User.objects.count()
        form.save()
        after_count = User.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(self.user.first_name, self.form_input['first_name'])
        self.assertEqual(self.user.last_name, self.form_input['last_name'])
        self.assertEqual(self.user.email, self.form_input['email'])
        self.assertEqual(self.user.bio, self.form_input['bio'])
