import pytest
from django.core.management import call_command
from rest_framework.test import APIClient

from factories import UserFactory, BicycleFactory, RentalFactory


@pytest.fixture(scope='session', autouse=True)
def django_db_setup(django_db_blocker):
    with django_db_blocker.unblock():
        call_command('migrate')


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_factory():
    return UserFactory


@pytest.fixture
def bicycle_factory():
    return BicycleFactory


@pytest.fixture
def rental_factory():
    return RentalFactory
