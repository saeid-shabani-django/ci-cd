import pytest
from rest_framework.test import APIClient, APIRequestFactory
from django.shortcuts import reverse
from ..models import Category
from accounts.models.profiles import Profile
from django.contrib.auth import get_user_model
User = get_user_model()

# @pytest.mark.django_db
# class TestPostApi:
#    client = APIClient()
#    def test_post_api(self):
      
#       resp = self.client.get(reverse('all_posts-list'))
#       assert resp.status_code == 200
      
#    def test_create_post(self):
#       url = reverse('all_posts-list')
#       category = Category.objects.create(name="cat1")
#       data={
#                 "author": 'aa'
#                 "content": "this is content",
#                 "title": "this is tile",
#                 "status": "done"
                
#             }
      
#       resp = self.client.post(url,data)
#       assert resp.status_code == 401
   # def test_create_post_authenticated(self):
   #    user = User.objects.create(email='dd@dd.com',password='S10011001sh')
   #    url = reverse('all_posts-list')
   #    self.client.force_authenticate(user=user)
   #    category = Category.objects.create(name="cat1")
   #    data={
   #              "content": "this is content",
   #              "title": "this is tile",
   #              "status": "done"
   #          }
   #    resp = self.client.post(url,data)
   #    assert resp.status_code == 201
      








