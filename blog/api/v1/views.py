from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from blog.models import Post, Category
from accounts.models import CustomUser
from .serializers import PostSerializer, UpdatedPostSerializer, CategorySerializer
from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
    AllowAny,
)
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.viewsets import ViewSet, ModelViewSet
from .permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .paginations import LargeResultsSetPagination
from .filters import PostFilter
from .serializers import ChangePasswordSerializer


class PostModelViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["title", "status"]
    search_fields = [
        "content",
    ]
    ordering_fields = ["title", "id", "content"]

    @action(detail=False, methods=["GET"])
    def saeid(self, request):
        post = Post.objects.filter(title__icontains="saeid")
        serializer = PostSerializer(post, many=True)
        return Response(serializer.data)


class CategoryModelViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsAdminUser]


class ChangePasswordView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self, query_set=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            password = serializer.data.get("old_password")
            print(password)
            print(self.get_object)
            if not self.object.check_password(password):
                return Response(
                    "the password is wrong, did you forget that? click here"
                )
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response("done")
        return Response(serializer.errors)
