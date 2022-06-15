from rest_framework_simplejwt.tokens import RefreshToken
from jwt import decode
from django.conf import settings


def encode_token(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }


def decode_token(request):
    token = request.headers.get('token')
    if not token:
        token = request.query_params.get('token')
    data = decode(token, settings.SECRET_KEY, 'HS256')
    user_id = data['user_id']
    return user_id

