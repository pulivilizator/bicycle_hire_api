from decimal import Decimal

from drf_spectacular.utils import extend_schema_serializer, extend_schema_field, OpenApiTypes
from rest_framework import serializers

from django.core.validators import MinValueValidator

from . import models


class BicycleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Bicycle
        fields = '__all__'


class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Rental
        fields = '__all__'
        read_only_fields = ['is_paid', 'total_price', 'start_time', 'end_time', 'user']
