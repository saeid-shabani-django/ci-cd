from django.urls import path, include
from .. import views

urlpatterns = [
    path("auth/", views.AllProfileUsers.as_view(), name="profile-list"),
    path("auth/users/<int:pk>/", views.UserProfileView.as_view(), name="user-profile"),
    path("token/", views.CustomTokenObtainPairView.as_view(), name="custom-auth"),
    # activation
    # resend actication
]
