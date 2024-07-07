from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Q
from django.utils import timezone

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import mixins, GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ValidationError
from rest_framework import status

from . import serializers, models
from .tasks import send_rental_ended_mail
from .schema import schema


@schema.bicycle_list_extend_schema
class BicycleViewSet(mixins.ListModelMixin,
                     GenericViewSet):
    queryset = models.Bicycle.available_bicycles.all()
    serializer_class = serializers.BicycleSerializer


@schema.common_rental_extend_schema
@schema.rental_create_extend_schema
class RentalViewSet(mixins.CreateModelMixin,
                    GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.RentalSerializer
    queryset = models.Rental.objects.all()

    def perform_create(self, serializer, *args, **kwargs):
        bicycle_id = self.request.data['bicycle']
        bicycle = models.Bicycle.objects.get(id=bicycle_id)
        self.check_rentals(bicycle)
        bicycle.available = False
        bicycle.save()
        serializer.save(user=self.request.user)

    @schema.return_bicycle_extend_schema
    @action(detail=False, methods=['patch'])
    def return_bicycle(self, request: WSGIRequest):
        try:
            rental = models.Rental.objects.get(user=self.request.user, end_time__isnull=True, is_paid=False)
        except models.Rental.DoesNotExist:
            return Response({'error': 'У пользователя нет активной аренды'}, status=status.HTTP_404_NOT_FOUND)
        bicycle = rental.bicycle
        rental.end_time = timezone.now()
        rental.total_price = rental.rental_total_price()
        bicycle.available = True
        rental.save()
        bicycle.save()
        send_rental_ended_mail.delay(rental_id=rental.id)
        return Response({'total_price': rental.total_price}, status=status.HTTP_200_OK)

    @schema.pay_rental_extend_schema
    @action(detail=False, methods=['patch'])
    def pay_rental(self, request: WSGIRequest, pk=None):
        """Условная оплата"""
        try:
            rental = models.Rental.objects.get(user=self.request.user, end_time__isnull=False, is_paid=False)
        except models.Rental.DoesNotExist:
            return Response({'error': 'У пользователя нет активной аренды'}, status=status.HTTP_404_NOT_FOUND)
        rental.is_paid = True
        rental.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @schema.rental_history_extend_schema
    @action(detail=False, methods=['get'])
    def rental_history(self, request: WSGIRequest):
        user = request.user
        rentals = models.Rental.objects.filter(user=user).order_by('-start_time')
        if not rentals.exists():
            return Response({'error': 'История аренды отсутствует'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(rentals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def check_rentals(self, bicycle: models.Bicycle):
        if models.Rental.objects.filter(Q(user=self.request.user) &
                                        (Q(end_time__isnull=True) | Q(is_paid=False))).exists():
            raise ValidationError('Пользователь уже имеет арендованный или неоплаченный велосипед')
        if not bicycle.available:
            raise ValidationError('Велосипед уже арендован')
