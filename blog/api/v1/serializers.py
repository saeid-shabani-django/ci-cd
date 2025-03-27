from rest_framework import serializers
from accounts.models import Profile
from ...models import Post, Category
from rest_framework import status
from django.contrib.auth import password_validation


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):

    snippet = serializers.ReadOnlyField(source="get_snippet")
    relative_url = serializers.URLField(source="get_absolute_api_url", read_only=True)
    absolute_url = serializers.SerializerMethodField()
    # category = serializers.SlugRelatedField(read_only=True, slug_field="name")

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "category",
            "content",
            "author",
            "snippet",
            "status",
            "relative_url",
            "absolute_url",
        ]

    author = serializers.SlugRelatedField(read_only=True, slug_field="first_name")

    def get_absolute_url(self, post):
        request = self.context.get("request")
        return request.build_absolute_uri(post.id)

    def to_representation(self, instance):
        request = self.context.get("request")
        rep = super().to_representation(instance)
        if request.method == "GET":

            pk = request.parser_context.get("kwargs").get("pk")
            if pk != None:
                rep.pop("snippet")
                rep.pop("absolute_url")
                rep.pop("relative_url")
                return rep

            else:
                rep.pop("content")
                return rep
        rep["category"] = CategorySerializer(instance.category).data

        return rep

    def create(self, validated_data):
        request = self.context.get("request").user.id
        validated_data["author"] = Profile.objects.get(user__id=request)
        return super().create(validated_data)


class UpdatedPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title", "content"]


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, max_length=255)
    new_password = serializers.CharField(required=True, max_length=255)
    new_password1 = serializers.CharField(required=True, max_length=255)

    def validate(self, attrs):
        if attrs.get("new_password") != attrs.get("new_password1"):
            raise serializers.ValidationError(
                {"password": status.HTTP_406_NOT_ACCEPTABLE}
            )
        try:
            password_validation(attrs.get("new_password"))
        except:
            raise serializers.ValidationError({"password": "choose another password"})

        return super().validate(attrs)
