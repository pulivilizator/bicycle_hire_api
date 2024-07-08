import pytest
from unittest.mock import patch
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from apps.bicycles.models import Bicycle


@pytest.mark.django_db
def test_bicycle_list(api_client, bicycle_factory):
    bicycle_factory.create_batch(5, available=True)
    response = api_client.get(reverse('rentals:bicycle-list'))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 5


@pytest.mark.django_db
def test_rental_create(api_client, user_factory, bicycle_factory):
    user = user_factory()
    bicycle = bicycle_factory()
    api_client.force_authenticate(user=user)
    response = api_client.post(reverse('rentals:rental-list'), data={'bicycle': bicycle.id})
    assert response.status_code == status.HTTP_201_CREATED
    assert not Bicycle.objects.get(id=bicycle.id).available


@pytest.mark.django_db
def test_rental_return(api_client, user_factory, bicycle_factory, rental_factory):
    user = user_factory()
    bicycle = bicycle_factory(available=False)
    rental = rental_factory(user=user, bicycle=bicycle, end_time=None, is_paid=False)
    api_client.force_authenticate(user=user)
    with patch('apps.bicycles.views.send_rental_ended_mail.delay') as mock_send_rental_ended_mail:
        response = api_client.patch(reverse('rentals:rental-return-bicycle'))
        assert response.status_code == status.HTTP_200_OK
        rental.refresh_from_db()
        assert rental.end_time is not None
        assert rental.total_price is not None
    assert Bicycle.objects.get(id=bicycle.id).available


@pytest.mark.django_db
def test_rental_pay(api_client, user_factory, bicycle_factory, rental_factory):
    user = user_factory()
    bicycle = bicycle_factory()
    rental = rental_factory(user=user, bicycle=bicycle, end_time=timezone.now(), is_paid=False)
    api_client.force_authenticate(user=user)
    response = api_client.patch(reverse('rentals:rental-pay-rental'))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    rental.refresh_from_db()
    assert rental.is_paid
