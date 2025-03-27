from django.urls import path, include, re_path

from .. import views

urlpatterns = [
    path("registration/", views.RegistrationApiView.as_view(), name="registration"),
    path("activate/confirm/", views.EmailSending.as_view(), name="email"),
    re_path(r"^activate/(.+)/$", views.activate, name="activate"),
    path("resend/activate/", views.resend_activation_code, name="activate"),
]
