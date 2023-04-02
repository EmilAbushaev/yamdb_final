from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken


def send_confirmation_code(user, email):
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Confirmation code',
        f'Код подтверждения: {confirmation_code}',
        'yamdb@example.com',
        [f'{email}'],
        fail_silently=False,
    )


def get_access_token(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)
