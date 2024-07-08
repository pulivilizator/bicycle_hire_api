import pytest
from decimal import Decimal
from apps.bicycles.serializers import BicycleSerializer, RentalSerializer
from apps.bicycles.models import Bicycle, Rental


@pytest.mark.django_db
def test_bicycle_serializer():
    bicycle = Bicycle.objects.create(available=True, price_per_minute=Decimal('1.50'))
    serializer = BicycleSerializer(bicycle)
    data = serializer.data
    assert data['available']
    assert data['price_per_minute'] == '1.50'


@pytest.mark.django_db
def test_rental_serializer(user_factory, bicycle_factory):
    user = user_factory()
    bicycle = bicycle_factory()
    rental = Rental.objects.create(bicycle=bicycle, user=user)
    serializer = RentalSerializer(rental)
    data = serializer.data
    assert data['bicycle'] == bicycle.id
    assert data['user'] == user.id
    assert 'start_time' in data
    assert data['end_time'] is None
    assert data['total_price'] is None
    assert not data['is_paid']
