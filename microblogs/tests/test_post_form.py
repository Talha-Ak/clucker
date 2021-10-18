from django.test import TestCase
from django import forms
from microblogs.forms import PostForm
from microblogs.models import User

class PostFormTestCase(TestCase):
    def setUp(self):
        self.form_input = {
            'text': 'This is an example "cluck" to be tested.'
        }

    def test_valid_post(self):
        form = PostForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_post_form_model_validation(self):
        self.form_input['text'] = 'x' * 281
        form = PostForm(data=self.form_input)
        self.assertFalse(form.is_valid())
