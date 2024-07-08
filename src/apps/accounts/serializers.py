from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers

from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=get_user_model().objects.all(), message='Email уже зарегистрирован')])
    name = serializers.CharField(max_length=255)
    surname = serializers.CharField(max_length=255)
    patronymic = serializers.CharField(max_length=255, required=False, allow_null=True, allow_blank=True)

    class Meta:
        model = get_user_model()
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def validate_password(self, value):
        try:
            validate_password(value)
            return value
        except DjangoValidationError as e:
            raise serializers.ValidationError(
                'Пароль должен состоять минимум из 8ми символов и содержать цифры, заглавные и строчные буквы')

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            surname=validated_data['surname'],
            patronymic=validated_data.get('patronymic', None),
            password=validated_data['password'],
        )
        return user
