from decimal import Decimal

from django.core.validators import MinValueValidator
from django.utils import timezone
from django.db import models
from django.db.models import Index
from django.conf import settings

from . import managers


class Bicycle(models.Model):
    available = models.BooleanField(default=True)
    price_per_minute = models.DecimalField(max_digits=3, decimal_places=2)

    objects = models.Manager()
    available_bicycles = managers.BicycleAvailableManager()

    def __str__(self):
        return f'{self.id} - {"available" if self.available else "rented"} - {self.price_per_minute}rub.'

    class Meta:
        verbose_name = 'Велосипед'
        verbose_name_plural = 'Велосипеды'

        indexes = (
            Index(fields=('available',)),
        )


class Rental(models.Model):
    bicycle = models.ForeignKey(Bicycle,
                                related_name='bicycles',
                                null=True,
                                on_delete=models.SET_NULL)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='users',
                             null=True,
                             on_delete=models.SET_NULL)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True, default=None)
    total_price = models.DecimalField(max_digits=8,
                                      decimal_places=2,
                                      null=True,
                                      blank=True,
                                      default=None)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f'Rent by user: {self.user.full_name()} bicycle №{self.bicycle.pk}'

    def rental_total_price(self):
        if self.end_time and self.start_time:
            result = Decimal((self.end_time - self.start_time).total_seconds() / 60) * self.bicycle.price_per_minute
            return result.quantize(Decimal('0.01'))
        return None

    class Meta:
        verbose_name = 'Аренда велосипеда'
        verbose_name_plural = 'Аренды велосипедов'
        indexes = (
            Index(fields=('-start_time',)),
        )
