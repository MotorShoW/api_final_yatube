from rest_framework import viewsets, filters, permissions, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from posts.models import Group, Post, User
from .permissions import IsAuthorOrReadOnly
from .serializers import (CommentSerializer, GroupSerializer, PostSerializer,
                          UserSerializer, FollowSerializer)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter
    )
    search_fields = ('title', 'description')
    ordering_fields = ('title', 'id')
    ordering = ('title',)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter
    )
    search_fields = ('text', 'group__title', 'author__username')
    ordering_fields = ('group', 'pub_date')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter
    )
    search_fields = ('text', 'author__username')
    ordering_fields = ('created',)

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments.all()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter
    )
    search_fields = (
        'username', 'date_joined', 'first_name', 'last_name', 'email'
    )
    ordering_fields = ('username', 'date_joined')
    ordering = ('-date_joined',)


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (
        filters.SearchFilter,
        filters.OrderingFilter
    )
    search_fields = ('user__username', 'following__username')
    ordering_fields = ('following__username', 'id')
    ordering = ('id',)

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
