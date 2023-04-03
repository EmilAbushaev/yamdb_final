import api.filters as af
import api.permissions as pm
import api.serializers as sr
import reviews.models as rm
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from users.models import User
from users.tokens import get_access_token, send_confirmation_code


class NoPutModelViewSet(viewsets.ModelViewSet):
    """
    Базовый вьюсет, предоставляющий все методы ModelViewSet, кроме PUT.
    """
    http_method_names = ['get', 'post', 'patch', 'delete', 'head', 'options']


class CategoryList(generics.ListCreateAPIView):
    queryset = rm.Category.objects.all()
    serializer_class = sr.CategorySerializer
    permission_classes = (pm.AdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class CategoryDelete(generics.DestroyAPIView):
    serializer_class = sr.CategorySerializer
    permission_classes = (pm.AdminOrReadOnly,)
    lookup_field = 'slug'

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return rm.Category.objects.filter(slug=slug)


class GenreList(generics.ListCreateAPIView):
    queryset = rm.Genre.objects.all()
    serializer_class = sr.GenreSerializer
    permission_classes = (pm.AdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class GenreDelete(generics.DestroyAPIView):
    serializer_class = sr.GenreSerializer
    permission_classes = (pm.AdminOrReadOnly,)
    lookup_field = 'slug'

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        return rm.Genre.objects.filter(slug=slug)


class TitleViewSet(NoPutModelViewSet):
    queryset = rm.Title.objects.all()
    permission_classes = (pm.AdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = af.TitleFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return sr.TitleListSerializer
        return sr.TitleSerializer


class ReviewViewSet(NoPutModelViewSet):
    serializer_class = sr.ReviewSerializer
    permission_classes = (pm.SafeOrAuthorOrExceedingRoleOnly,)

    def get_queryset(self):
        title = get_object_or_404(rm.Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def title_rating(self):
        title = get_object_or_404(rm.Title, pk=self.kwargs.get('title_id'))
        reviews = title.reviews.all()
        rating_sum = 0
        for review in reviews:
            rating_sum += review.score
        title.rating = int(rating_sum / len(reviews))
        title.save()

    def perform_create(self, serializer):
        title = get_object_or_404(
            rm.Title,
            pk=self.kwargs.get('title_id')
        )
        author = self.request.user
        if rm.Review.objects.filter(author=author, title=title.pk).exists():
            raise ValidationError
        serializer.save(
            author=author,
            title_id=title.pk
        )
        self.title_rating()


class CommentViewSet(NoPutModelViewSet):
    serializer_class = sr.CommentSerializer
    permission_classes = (pm.SafeOrAuthorOrExceedingRoleOnly,)

    def get_queryset(self):
        review = get_object_or_404(
            rm.Review,
            pk=self.kwargs.get('review_id')
        )
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            rm.Review,
            pk=self.kwargs.get('review_id')
        )
        serializer.save(
            author=self.request.user,
            review_id=review.pk
        )


class SignUp(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = sr.SignUpSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not (User.objects.filter(
                username=serializer.validated_data['username']
        )
                and User.objects.filter(
                    email=serializer.validated_data['email'])
        ):
            self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        email = serializer.data['email']
        user = User.objects.get(username=serializer.data['username'])
        send_confirmation_code(user, email)
        return Response(
            serializer.data, status=status.HTTP_200_OK, headers=headers
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def get_jwt_token(request):
    serializer = sr.TokenSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    username = serializer.data.get('username')
    confirmation_code = serializer.data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, confirmation_code):
        token = get_access_token(user)
        return Response(
            {'token': str(token)}, status=status.HTTP_200_OK
        )

    return Response(
        {'confirmation_code': 'Неверный код подтверждения'},
        status=status.HTTP_400_BAD_REQUEST
    )


class UsersViewSet(NoPutModelViewSet):
    queryset = User.objects.all()
    serializer_class = sr.UserSerializer
    permission_classes = (pm.IsAdmin,)
    lookup_field = 'username'
    filter_backends = (SearchFilter,)
    search_fields = ('username',)

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        user = get_object_or_404(User, username=request.user.username)
        serializer = self.get_serializer(user)
        if request.method == 'PATCH':
            serializer = sr.UserPatchSerializer(
                user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)
