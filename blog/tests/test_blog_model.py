from django.test import TestCase
from ..models import Post, Category
from accounts.models.profiles import Profile
from django.contrib.auth import get_user_model
from django.shortcuts import reverse

User = get_user_model()


class TestModel(TestCase):
    def setUp(self):
        self.custom_user = User.objects.create(
            email="saeid@saeid.com", password="S10011001sh"
        )

        self.profile_obj = Profile.objects.create(
            user=self.custom_user,
            first_name="saeid",
            last_name="shabani",
            description="this is description",
        )
        self.category = Category.objects.create(name="cat2")

        self.post = Post.objects.create(
            author=self.profile_obj,
            content="this is content",
            title="this is title",
            category=self.category,
            status="done",
        )

    def test_post_model_with_valid_data(self):
        self.assertTrue(Post.objects.filter(pk=self.post.pk).exists())

    def test_post_detail_view(self):
        self.client.force_login(self.custom_user)
        resp = self.client.get(reverse("post_detail", kwargs={"pk": self.post.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.post.title)
        self.assertTemplateUsed(resp, "blog/detail.html")
