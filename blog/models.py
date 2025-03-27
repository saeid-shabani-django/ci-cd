from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


class Post(models.Model):
    author = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)
    # image = models.ImageField(null=True,blank=True)
    content = models.TextField()
    title = models.CharField(max_length=200)
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})

    def get_snippet(self):
        return self.content[:9]

    def get_absolute_api_url(self):
        return reverse("posts-detail", kwargs={"pk": self.pk})


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
