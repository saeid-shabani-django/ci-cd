from django.urls import path
from . import views


urlpatterns = [
    path("posts/", views.ShowPost.as_view(), name="post"),
    path("posts/<int:pk>/", views.ShowPostDetail.as_view(), name="post_detail"),
    path("form/", views.ShowCreateView.as_view(), name="create"),
    path("update/<int:pk>/", views.ShowUpdateView.as_view(), name="update"),
    path("delete/<int:pk>/", views.ShowDeleteView.as_view(), name="delete"),
]
