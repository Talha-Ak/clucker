from django.test import TestCase
from django.urls import reverse
from microblogs.forms import ProfileUpdateForm
from microblogs.models import User
from microblogs.tests.helpers import reverse_with_next

class UpdateProfileViewTestCase(TestCase):
    """Test suite for update_profile view"""

    fixtures = ['microblogs/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('update_profile')
        self.user = User.objects.get(username='@johndoe')
        self.form_input = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@otherdomain.com',
            'bio': 'Hello, this is my new bio.',
        }

    def test_update_profile_url(self):
        self.assertEqual(self.url, '/update_profile/')

    def test_get_update_profile(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, ProfileUpdateForm))
        self.assertFalse(form.is_bound)

    def test_get_update_profile_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_update_fail(self):
        self.client.login(username=self.user.username, password='Password123')
        self.form_input['email'] = 'bad@$invalid@email'
        response = self.client.post(self.url, self.form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'update_profile.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, ProfileUpdateForm))
        self.assertTrue(form.is_bound)
        self.assertNotEqual(self.user.email, self.form_input['email'])

    def test_update_pass(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.post(self.url, self.form_input, follow=True)
        response_url = reverse('feed')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')
        self.user = User.objects.get(username='@johndoe')  # Re-fetch user
        self.assertEqual(self.user.email, self.form_input['email'])
        self.assertEqual(self.user.bio, self.form_input['bio'])
