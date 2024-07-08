import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(
        email="test@example.com",
        name="Test",
        surname="User",
        password="Password123!"
    )
    assert user.email == "test@example.com"
    assert user.name == "Test"
    assert user.surname == "User"
    assert user.check_password("Password123!")
    assert user.is_active
    assert not user.is_admin


@pytest.mark.django_db
def test_full_name():
    user = User.objects.create_user(
        email="test@example.com",
        name="Test",
        surname="User",
        patronymic="Patronymic",
        password="Password123!"
    )
    assert user.full_name() == "User Test Patronymic"
