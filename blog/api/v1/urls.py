from django.urls import path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
urlpatterns = [
    path("change-password/", views.ChangePasswordView.as_view(), name="change-password")
    # path('posts/',views.GenericPostListView.as_view(),name='posts'),
    # path('posts/<int:pk>/',views.GenericPostListDetail.as_view(),name="post_detail"),
]
router.register("posts", views.PostModelViewSet,basename="all_posts")
router.register("categories", views.CategoryModelViewSet, basename="category")

print(router.urls)
urlpatterns += router.urls
