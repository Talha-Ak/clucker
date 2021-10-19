from django.test import TestCase
from django import forms
from microblogs.forms import PostForm
from microblogs.models import User, Post

class PostFormTestCase(TestCase):
    def setUp(self):
        self.form_input = {
            'text': 'This is an example "cluck" to be tested.'
        }

    def test_valid_post(self):
        form = PostForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = PostForm()
        self.assertIn('text', form.fields)
        text_widget = form.fields['text'].widget
        self.assertTrue(isinstance(text_widget, forms.Textarea))

    def test_post_form_model_validation(self):
        self.form_input['text'] = 'x' * 281
        form = PostForm(data=self.form_input)
        self.assertFalse(form.is_valid())
