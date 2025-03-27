from django.test import TestCase
from ..forms import CreatePost
from ..models import Category


class TestForm(TestCase):

    def test_form_with_valid_data(self):
        category = Category.objects.create(name="cat1")
        post = CreatePost(
            data={
                "content": "this is content",
                "title": "this is tile",
                "status": "done",
                "category": category,
            }
        )
        self.assertTrue(post.is_valid())

    def test_form_with_no_data(self):
        category = Category.objects.create(name="cat1")
        post = CreatePost()

        self.assertFalse(post.is_valid())
