import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_full_registration_cycle(api_client):
    data = {
        'email': 'test@example.com',
        'name': 'Test',
        'surname': 'User',
        'password': 'Password123!'
    }

    registration_response = api_client.post(reverse('accounts:registration'), data=data)
    assert registration_response.status_code == status.HTTP_201_CREATED
    assert 'access' in registration_response.data
    assert 'refresh' in registration_response.data
    assert get_user_model().objects.all().count() == 1

    login_response = api_client.post(reverse('accounts:login'),
                                     data={'email': data['email'], 'password': data['password']})
    assert login_response.status_code == status.HTTP_200_OK
    assert 'access' in login_response.data
    assert 'refresh' in login_response.data

    refresh_response = api_client.post(reverse('accounts:token_refresh'), {'refresh': login_response.data['refresh']})
    assert refresh_response.status_code == status.HTTP_200_OK
    assert 'access' in refresh_response.data
    assert 'refresh' in refresh_response.data

    logout_response = api_client.post(reverse('accounts:logout'),
                                      data={'refresh_token': refresh_response.data['refresh']})
    assert logout_response.status_code == status.HTTP_204_NO_CONTENT
