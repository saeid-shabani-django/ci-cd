from django.urls import path, include
from . import views


urlpatterns = [
    path("new/", views.show_view),
    path("api/v1/", include("accounts.api.v1.urls")),
    path("token/login/", views.CustomAuthToken.as_view(), name="login"),
    path("token/logout/", views.CustomAuthLogout.as_view(), name="logout"),
    path("api/v2/", include("djoser.urls")),
    path("api/v2/", include("djoser.urls.jwt")),
]
