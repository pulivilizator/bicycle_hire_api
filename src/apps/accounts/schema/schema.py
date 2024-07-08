from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from rest_framework import status

from . import serializers
from apps.accounts.serializers import UserSerializer

login_extend_schema = extend_schema(
    tags=['Authorization'],
    summary='Вход в аккаунт',
    request=serializers.LoginSerializer,
    responses={
        status.HTTP_200_OK: serializers.LoginRegisterResponse200Serializer,
        status.HTTP_400_BAD_REQUEST: serializers.LoginRegisterResponse400Serializer,
        status.HTTP_401_UNAUTHORIZED: serializers.LoginRegisterResponse400Serializer
    },
    examples=[
        OpenApiExample(
            name='Пример данных входа',
            value={
                'email': 'test@example.com',
                'password': 'Password123!'
            },
            summary='Пример запроса для входа',
            request_only=True,
        ),
    ]
)

registration_extend_schema = extend_schema(
    tags=['Authorization'],
    summary='Регистрация нового пользователя',
    request=UserSerializer,
    responses={
        status.HTTP_201_CREATED: serializers.LoginRegisterResponse200Serializer,
        status.HTTP_400_BAD_REQUEST: serializers.LoginRegisterResponse400Serializer
    },
    examples=[
        OpenApiExample(
            name='Пример данных регистрации',
            value={
                'email': 'test@example.com',
                'name': 'Test',
                'surname': 'User',
                'password': 'Password123!'
            },
            summary='Пример запроса для регистрации',
            request_only=True,
        ),
        OpenApiExample(
            name='Пример данных регистрации №2',
            value={
                'email': 'test@example.com',
                'name': 'Test',
                'surname': 'User',
                'patronymic': 'Patronymic',
                'password': 'Password123!'
            },
            summary='Пример запроса для регистрации №2',
            request_only=True,
        ),
    ]
)

logout_extend_schema = extend_schema(
    tags=['Authorization'],
    summary='Выход из аккаунта',
    request=serializers.LogoutSerializer,
    responses={
        status.HTTP_204_NO_CONTENT: None,
        status.HTTP_400_BAD_REQUEST: serializers.LoginRegisterResponse400Serializer
    }
)