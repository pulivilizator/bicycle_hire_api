import pytest
from django.utils import timezone
from decimal import Decimal
from apps.bicycles.models import Bicycle, Rental


@pytest.mark.django_db
def test_bicycle_str():
    bicycle = Bicycle.objects.create(available=True, price_per_minute=Decimal('1.50'))
    assert str(bicycle) == f'{bicycle.id} - available - 1.50rub.'


@pytest.mark.django_db
def test_rental_str(user_factory, bicycle_factory):
    user = user_factory()
    bicycle = bicycle_factory()
    rental = Rental.objects.create(bicycle=bicycle, user=user)
    assert str(rental) == f'Rent by user: {user.full_name()} bicycle №{bicycle.pk}'


@pytest.mark.django_db
def test_rental_total_price(user_factory, bicycle_factory):
    user = user_factory()
    bicycle = bicycle_factory(price_per_minute=Decimal('2.00'))
    start_time = timezone.now() - timezone.timedelta(minutes=30)
    end_time = timezone.now()
    rental = Rental.objects.create(
        bicycle=bicycle,
        user=user,
        start_time=start_time,
        end_time=end_time
    )
    assert rental.rental_total_price() == Decimal('60.00')
