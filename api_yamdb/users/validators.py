from rest_framework import serializers
from users.models import User


def validate_sign_up(data):
    if data['username'] in ['me', 'Me', 'ME', 'mE']:
        raise serializers.ValidationError(
            f'Username {data["username"]} is not valid'
        )
    if (User.objects.filter(username=data['username'])
            and not User.objects.filter(email=data['email'])):
        raise serializers.ValidationError('username занят')
    if (User.objects.filter(email=data['email'])
            and not User.objects.filter(username=data['username'])):
        raise serializers.ValidationError('email занят')
    return data


def validate_user_serializer(data):
    if 'username' in data or 'email' in data:
        if (User.objects.filter(username=data['username'])
                or User.objects.filter(email=data['email'])):
            raise serializers.ValidationError('username или email занят')
    return data


def validate_role(value):
    if value not in ['user', 'moderator', 'admin']:
        raise serializers.ValidationError('Несуществующая роль')
    return value
