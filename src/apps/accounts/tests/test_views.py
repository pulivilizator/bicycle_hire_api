import pytest
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_registration_api_view(api_client):
    url = reverse('accounts:registration')
    data = {
        'email': 'test@example.com',
        'name': 'Test',
        'surname': 'User',
        'password': 'Password123!'
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert 'refresh' in response.data
    assert 'access' in response.data


@pytest.mark.django_db
def test_login_api_view(api_client):
    user = User.objects.create_user(
        email="test@example.com",
        name="Test",
        surname="User",
        password="Password123!"
    )
    url = reverse('accounts:login')
    data = {
        'email': 'test@example.com',
        'password': 'Password123!'
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    assert 'refresh' in response.data
    assert 'access' in response.data


@pytest.mark.django_db
def test_logout_api_view(api_client):
    user = User.objects.create_user(
        email="test@example.com",
        name="Test",
        surname="User",
        password="Password123!"
    )
    url = reverse('accounts:login')
    data = {
        'email': 'test@example.com',
        'password': 'Password123!'
    }
    response = api_client.post(url, data, format='json')
    refresh_token = response.data['refresh']

    url = reverse('accounts:logout')
    data = {
        'refresh_token': refresh_token
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_204_NO_CONTENT
