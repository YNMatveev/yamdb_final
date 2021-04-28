from django.db.models import Avg
from django.shortcuts import get_object_or_404

from rest_framework.viewsets import (
    ModelViewSet,
    GenericViewSet
)
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
)
from rest_framework import permissions
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    Category,
    Genre,
    Title,
    Review
)

from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleListSerializer,
    TitleCreateSerializer,
    ReviewSerializer,
    CommentSerializer
)

from users.permissions import (
    IsAdminOrSuperUserSafe,
    IsOwnerOrAdminRole
)

from .filters import TitleFilter


class CRDMixin(CreateModelMixin,
               ListModelMixin,
               DestroyModelMixin,
               GenericViewSet):
    queryset = None
    serializer_class = None
    filter_backends = [SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrSuperUserSafe,
    ]


class CategoryViewSet(CRDMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CRDMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrSuperUserSafe,
    ]

    serializer_class = TitleListSerializer
    create_serializer_class = TitleCreateSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('-id')

    def get_serializer_class(self):
        if self.action in ['create', 'patch', 'update', 'partial_update']:
            return self.create_serializer_class
        return self.serializer_class


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrAdminRole,
    ]

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, review=review)

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()


class ReviewViewSet(ModelViewSet):
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrAdminRole,
    ]
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()
