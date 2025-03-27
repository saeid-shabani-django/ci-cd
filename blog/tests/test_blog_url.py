from django.test import TestCase
from ..views import ShowPostDetail, ShowPost
from django.urls import reverse, resolve
from ..models import Post
from accounts.models.profiles import Profile
from blog.models import Category


class TestUrl(TestCase):

    def test_url_blog(self):
        url = reverse("post_detail", kwargs={"pk": 1})
        self.assertEqual(resolve(url).func.view_class, ShowPostDetail)

    def test_post_list(self):
        url = reverse("post")
        self.assertEqual(resolve(url).func.view_class, ShowPost)
