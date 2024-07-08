from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

app_name = 'accounts'

router = DefaultRouter()
router.register(
    'password_reset',
    views.ResetPasswordRequestTokenSchemaViewSet,
    basename='reset-password-request'
)
router.register(
    "password_reset/validate_token",
    views.ResetPasswordValidateTokenSchemaViewSet,
    basename='reset-password-validate'
)
router.register(
    "password_reset/confirm",
    views.ResetPasswordConfirmSchemaViewSet,
    basename='reset-password-confirm',
)

v1_urlpatterns = [
    path('api/token/refresh/', views.TokenRefreshSchemaView.as_view(), name='token_refresh'),
    path('auth/registration/', views.RegistrationAPIView.as_view(), name='registration'),
    path('auth/login/', views.LoginAPIView.as_view(), name='login'),
    path('auth/logout/', views.LogoutAPIView.as_view(), name='logout'),
    *router.urls,
]
