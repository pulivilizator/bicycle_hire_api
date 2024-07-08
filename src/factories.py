from django.conf import settings
from django.utils import timezone

from decimal import Decimal
import factory


from apps.bicycles.models import Bicycle, Rental


class UserFactory(factory.django.DjangoModelFactory):
    name = factory.Faker('first_name')
    surname = factory.Faker('last_name')
    email = factory.Faker('email')
    password = factory.django.Password('pw')

    class Meta:
        model = settings.AUTH_USER_MODEL


class BicycleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Bicycle

    available = True
    price_per_minute = Decimal('5')


class RentalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Rental

    bicycle = factory.SubFactory(BicycleFactory)
    user = factory.SubFactory(UserFactory)
    start_time = factory.LazyFunction(timezone.now)
    end_time = None
    total_price = None
    is_paid = False
