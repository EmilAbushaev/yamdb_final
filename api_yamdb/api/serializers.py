import reviews.models as review_models
import reviews.validators as reviews_validators
import users.validators as users_validators
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers
from users.models import User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = review_models.Category
        fields = ('name', 'slug',)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = review_models.Genre
        fields = ('name', 'slug',)


class TitleSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=review_models.Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=review_models.Category.objects.all()
    )
    year = serializers.IntegerField(
        validators=[reviews_validators.validate_year]
    )

    class Meta:
        model = review_models.Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category',
        )
        read_only_fields = ('rating',)


class TitleListSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = review_models.Title
        fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category',
        )
        read_only_fields = (
            'id', 'name', 'year', 'rating', 'description', 'genre', 'category',
        )


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = review_models.Review
        fields = ('id', 'text', 'author', 'score', 'pub_date',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = review_models.Comment
        fields = ('id', 'text', 'author', 'pub_date')


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=[UnicodeUsernameValidator()],
    )
    email = serializers.EmailField(
        max_length=254,
    )

    def validate(self, data):
        return users_validators.validate_sign_up(data)

    class Meta:
        model = User
        fields = ('email', 'username',)


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=150,
        validators=[UnicodeUsernameValidator()],
    )
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
        validators=[UnicodeUsernameValidator()],
    )
    email = serializers.EmailField(
        max_length=254
    )
    first_name = serializers.CharField(
        required=False,
        max_length=150,
    )
    last_name = serializers.CharField(
        required=False,
        max_length=150,
    )
    bio = serializers.CharField(
        required=False,
    )
    role = serializers.CharField(
        default='user',
        validators=[users_validators.validate_role]
    )

    def validate(self, data):
        return users_validators.validate_user_serializer(data)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class UserPatchSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=False,
        max_length=150,
        validators=[UnicodeUsernameValidator()],
    )
    email = serializers.EmailField(
        required=False,
        max_length=254
    )
    first_name = serializers.CharField(
        required=False,
        max_length=150,
    )
    last_name = serializers.CharField(
        required=False,
        max_length=150,
    )
    bio = serializers.CharField(
        required=False,
    )
    role = serializers.CharField(
        required=False,
        read_only=True,
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )
