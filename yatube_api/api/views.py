from rest_framework import permissions, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404

from posts.models import Follow, Group, Post

from .paginator import MyPaginator
from .permissions import OwnerOrSafeMethods
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        OwnerOrSafeMethods,
        permissions.IsAuthenticatedOrReadOnly,
    )
    pagination_class = MyPaginator

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FollowViewSet(PostViewSet):
    model = Follow
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated, )
    filter_backends = (SearchFilter, )
    search_fields = ('following__username', )
    pagination_class = None

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    pagination_class = None


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        OwnerOrSafeMethods,
        permissions.IsAuthenticatedOrReadOnly
    )
    pagination_class = None

    def get_queryset(self):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        return post.comments.all()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        serializer.save(
            author=self.request.user,
            post_id=post.id
        )
