from rest_framework.serializers import ModelSerializer
from ...models import Profile, CustomUser
from django.core.exceptions import ValidationError
from django.core import exceptions
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


class RegistraionSerializer(ModelSerializer):
    password1 = serializers.CharField(max_length=120, write_only=True)

    class Meta:
        model = CustomUser
        fields = ["email", "password", "password1"]

    def validate(self, attrs):
        password1 = attrs.get("password1")
        if password1 != attrs.get("password"):
            raise ValidationError("passwords does not match")
        try:
            validate_password(attrs.get("password"))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({"password": e.messages})
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop("password1", None)
        return CustomUser.objects.create_user(**validated_data)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    token_class = RefreshToken

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        request = self.context.get("request")

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        data["email"] = str(self.user.email)
        data["id"] = str(self.user.id)
        return data


class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ("email",)
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate_email(self, value):
        user = self.context["request"].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError(
                {"email": "This email is already in use."}
            )
        return value

    def update(self, instance, validated_data):
        instance.first_name = validated_data["first_name"]
        instance.last_name = validated_data["last_name"]
        instance.email = validated_data["email"]
        if not user.is_verified:
            msg = "your account is not verified"
            raise serializers.ValidationError(msg, code="varification")

        instance.save()

        return instance


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "first_name", "last_name"]


class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(label=("email"), write_only=True)
    password = serializers.CharField(
        label=("Password"),
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
    )
    token = serializers.CharField(label=("Token"), read_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"), email=email, password=password
            )

            if not user:
                msg = "Unable to log in with provided credentials.try again !!"
                raise serializers.ValidationError(msg, code="authorization")
            if not user.is_verified:
                msg = "your account is not verified"
                raise serializers.ValidationError(msg, code="varification")
            token, _ = Token.objects.get_or_create(user=user)
            attrs["token"] = token.key

        else:
            msg = 'Must include "username" and "password".'
            raise serializers.ValidationError(msg, code="authorization")

        return attrs


class ResendActivationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "email",
        ]
