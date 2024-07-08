import pytest
from unittest.mock import patch
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from apps.bicycles.models import Rental


@pytest.mark.django_db
def test_full_rental_cycle(api_client, user_factory, bicycle_factory):
    user = user_factory()
    bicycle = bicycle_factory()

    api_client.force_authenticate(user=user)

    response = api_client.post(reverse('rentals:rental-list'), data={'bicycle': bicycle.id})
    assert response.status_code == status.HTTP_201_CREATED
    rental_id = response.data['id']

    bicycle.refresh_from_db()
    assert not bicycle.available

    with patch('apps.bicycles.views.send_rental_ended_mail.delay') as mock_send_rental_ended_mail:
        response = api_client.patch(reverse('rentals:rental-return-bicycle'))
        assert response.status_code == status.HTTP_200_OK
        rental = Rental.objects.get(id=rental_id)
        assert rental.end_time is not None
        assert rental.total_price is not None

    # response = api_client.patch(reverse('rentals:rental-return-bicycle'))
    # assert response.status_code == status.HTTP_200_OK
    # rental = Rental.objects.get(id=rental_id)
    # assert rental.end_time is not None
    # assert rental.total_price is not None

    bicycle.refresh_from_db()
    assert bicycle.available

    response = api_client.patch(reverse('rentals:rental-pay-rental'))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    rental.refresh_from_db()
    assert rental.is_paid


@pytest.mark.django_db
def test_rental_history(api_client, user_factory, rental_factory):
    user = user_factory()
    rental_factory.create_batch(5, user=user, end_time=timezone.now(), is_paid=True)

    api_client.force_authenticate(user=user)

    response = api_client.get(reverse('rentals:rental-rental-history'))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 5


@pytest.mark.django_db
def test_check_rentals(api_client, user_factory, bicycle_factory, rental_factory):
    user = user_factory()
    bicycle = bicycle_factory()
    rental = rental_factory(user=user, bicycle=bicycle, end_time=None, is_paid=False)

    api_client.force_authenticate(user=user)

    response = api_client.post(reverse('rentals:rental-list'), data={'bicycle': bicycle.id})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
