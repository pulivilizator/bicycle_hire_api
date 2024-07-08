from django.contrib.auth import authenticate

from drf_spectacular.utils import extend_schema

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from django_rest_passwordreset.views import (ResetPasswordConfirmViewSet, ResetPasswordRequestTokenViewSet,
                                             ResetPasswordValidateTokenViewSet)
from rest_framework_simplejwt.views import TokenRefreshView

from .serializers import UserSerializer
from .schema import schema


@schema.registration_extend_schema
class RegistrationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            refresh.payload.update({
                'user_id': user.id,
                'email': user.email
            })
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_201_CREATED)
        return Response({
            'error': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


@schema.login_extend_schema
class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        email = data.get('email', None)
        password = data.get('password', None)
        if not email or not password:
            return Response({'error': 'Отсутствует логин или пароль'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=email, password=password)
        if user is None:
            return Response({'error': 'Неверные данные'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        refresh.payload.update({
            'user_id': user.id,
            'email': user.email
        })

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }, status=status.HTTP_200_OK)


@schema.logout_extend_schema
class LogoutAPIView(APIView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({'error': 'Необходим refresh token'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response({'error': 'Неверный refresh token'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(
    tags=['Authorization'],
    summary='Замена устаревшего токена авторизации',
    description='Принимает токен refresh и возвращает токен новую пару токенов'
)
class TokenRefreshSchemaView(TokenRefreshView):
    pass



@extend_schema(
    tags=['Password reset'],
    summary='Метод для запроса сброса пароля с отправкой токена на email',
    description='Api предоставляющий метод для запроса токена сброса пароля на основе адреса '
                'электронной почты\n\nОтправляет сигнал reset_password_token_created, когда токен сброса был создан'
)
class ResetPasswordRequestTokenSchemaViewSet(ResetPasswordRequestTokenViewSet):
    pass

@extend_schema(
    tags=['Password reset'],
    summary='Установка нового пароля на основе токена',
    description='Api предоставляющий метод сброса пароля на основе уникального токена'
)
class ResetPasswordConfirmSchemaViewSet(ResetPasswordConfirmViewSet):
    pass

@extend_schema(
    tags=['Password reset'],
    summary='Проверка действительности токена',
    description='Api предоставляющий метод для проверки действительности токена'
)
class ResetPasswordValidateTokenSchemaViewSet(ResetPasswordValidateTokenViewSet):
    pass
