from rest_framework import serializers


class ReturnBicycleSchemaSerializer(serializers.Serializer):
    total_price = serializers.DecimalField(max_digits=8, decimal_places=2)


class CreateRentalSchemaSerializer(serializers.Serializer):
    bicycle = serializers.IntegerField()


class NotFoundSchemaSerializer(serializers.Serializer):
    error = serializers.CharField()


class UnauthorizedSchemaSerializer(serializers.Serializer):
    detail = serializers.CharField()
