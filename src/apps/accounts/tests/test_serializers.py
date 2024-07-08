import pytest
from apps.accounts.serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_user_serializer_create():
    data = {
        'email': 'test@example.com',
        'name': 'Test',
        'surname': 'User',
        'password': 'Password123!'
    }
    serializer = UserSerializer(data=data)
    assert serializer.is_valid()
    user = serializer.save()
    assert user.email == 'test@example.com'
    assert user.name == 'Test'
    assert user.surname == 'User'
    assert user.check_password('Password123!')


@pytest.mark.django_db
def test_user_serializer_validation_error():
    data = {
        'email': 'test@example.com',
        'name': 'Test',
        'surname': 'User',
        'password': 'pass'
    }
    serializer = UserSerializer(data=data)
    assert not serializer.is_valid()
    assert 'password' in serializer.errors
