from rest_framework.viewsets import ModelViewSet, generics
from ...models import Profile, CustomUser
from django.core.mail import send_mail
from .serializers import RegistraionSerializer, UpdateUserSerializer, ProfileSerializer
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from django.conf import settings
from .tokens import account_activation_token
from .serializers import RegistraionSerializer
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import *
from rest_framework.views import Response
from django.http import HttpResponse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import reverse
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenViewBase
from .serializers import CustomTokenObtainPairSerializer, CustomAuthTokenSerializer
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from ..utils import EmailThreading
from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken
from rest_framework_simplejwt.exceptions import (
    InvalidToken,
    TokenError,
    TokenBackendError,
)
from rest_framework.decorators import api_view
import jwt
from datetime import datetime, timedelta


class RegistrationApiView(generics.GenericAPIView):
    serializer_class = RegistraionSerializer

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return {
            "access": str(refresh.access_token),
        }

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        activation_url = self.get_tokens_for_user(user)["access"]
        context = {
            "username": user.email,
            "activation_url": activation_url,
            "email_body": f"http://127.0.0.1:8000/accounts/api/v1/activate/{activation_url}",
        }
        html_content = render_to_string("accounts/email.html", context)
        email = EmailMultiAlternatives(
            subject="Email Activation",
            body=f"click on link below to active your account ",
            from_email="noreply@example.com",
            to=[user.email],
        )
        email.attach_alternative(html_content, "text/html")

        # EmailThreading(email_obj=email).start()
        email.send()
        return Response("email sent successfully ")


class CustomTokenObtainPairView(TokenViewBase):
    permission_classes = ()
    authentication_classes = ()

    serializer_class = CustomAuthTokenSerializer
    # _serializer_class = ""

    # www_authenticate_realm = "api"

    def get_serializer_class(self):
        """
        If serializer_class is set, use it directly. Otherwise get the class from settings.
        """

        if self.serializer_class:
            return self.serializer_class
        try:
            return import_string(self._serializer_class)
        except ImportError:
            msg = f"Could not import serializer '{self._serializer_class}'"
            raise ImportError(msg)

    def get_authenticate_header(self, request):
        return '{} realm="{}"'.format(
            AUTH_HEADER_TYPES[0],
            self.www_authenticate_realm,
        )

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]


class AllProfileUsers(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class EmailSending(generics.GenericAPIView):
    serializer_class = RegistraionSerializer

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return {
            "access": str(refresh.access_token),
        }

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        activation_url = self.get_tokens_for_user(user)["access"]
        context = {
            "username": user.email,
            "activation_url": activation_url,
            "email_body": f"http://127.0.0.1:8000/accounts/api/v1/activate/{activation_url}",
        }
        html_content = render_to_string("accounts/email.html", context)
        email = EmailMultiAlternatives(
            subject="Email Activation",
            body=f"click on link below to active your account ",
            from_email="noreply@example.com",
            to=[user.email],
        )
        email.attach_alternative(html_content, "text/html")

        # EmailThreading(email_obj=email).start()
        email.send()
        return Response("email sent successfully ")


@api_view()
def activate(request, jwt_token):
    User = get_user_model()
    token = jwt_token

    try:
        user_id = UntypedToken(token)["user_id"]
        user = User.objects.get(pk=user_id)

        if user.is_verified:
            return Response("this link has been used before !")
        user.is_verified = True
        user.is_active = True
        user.save()
        return Response(token)
    except (InvalidToken, TokenError, TokenBackendError) as e:
        Response("Invalid token:", status=status.HTTP_400_BAD_REQUEST)


@api_view()
def resend_activation_code(request):
    user = request.user

    if not request.user.is_authenticated:
        return Response("please login first ")

    User = get_user_model()
    payload = {
        "user_id": user.id,
        "email": user.email,
        "exp": datetime.utcnow() + timedelta(days=1),  # Expiration time (1 day)
        "iat": datetime.now(),  # Issued at time
    }

    # Encode the payload into a JWT token using a secret key (should be stored securely in settings)
    token = jwt.encode(
        payload,
        "django-insecure-#8m$$6dq%&)g(3j%6lb899j&2ixqs2oux-qh&boh2eq@(&!)8xv",
        algorithm="HS256",
    )

    try:
        if user.is_verified:
            return Response(token)
    except:
        return Response("user credentials is not provided")
