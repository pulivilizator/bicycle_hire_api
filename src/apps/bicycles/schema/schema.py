from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiParameter, OpenApiTypes
from rest_framework import status

from . import serializers
from apps.bicycles.serializers import RentalSerializer


common_rental_extend_schema = extend_schema(
    tags=['Rental'],
    parameters=[
        OpenApiParameter(
            name='Bearer access token',
            location=OpenApiParameter.HEADER,
            type=str,
            description='Токен доступа',
        )
    ]
)

bicycle_list_extend_schema = extend_schema(
    summary='Список доступных велосипедов',
    tags=['Bicycles'],
    examples=[
        OpenApiExample(
            name='Пример возвращаемых данных',
            value={
                'id': 1,
                'available': True,
                "price_per_minute": "5.00"
            },
        ),
    ]
)

return_bicycle_extend_schema = extend_schema(
    summary='Возврат велосипеда',
    description='Возврат велосипеда текущей аренды пользователя\n\nДля возврата необходима авторизация',
    request=None,
    responses={
        status.HTTP_200_OK: serializers.ReturnBicycleSchemaSerializer,
        status.HTTP_404_NOT_FOUND: serializers.NotFoundSchemaSerializer,
        status.HTTP_401_UNAUTHORIZED: serializers.UnauthorizedSchemaSerializer
    },
    examples=[
        OpenApiExample(
            name='Пример возвращаемых данных',
            value={
                'total_price': '505.10'
            }
        )
    ]
)

pay_rental_extend_schema = extend_schema(
    summary='Оплата аренды',
    description='Оплата текущей аренды пользователя\n\nДля оплаты необходима авторизация',
    request=None,
    responses={
        status.HTTP_204_NO_CONTENT: None,
        status.HTTP_404_NOT_FOUND: serializers.NotFoundSchemaSerializer,
        status.HTTP_401_UNAUTHORIZED: serializers.UnauthorizedSchemaSerializer
    },
)

rental_history_extend_schema = extend_schema(
    summary='История аренд',
    description='Получение истории аренд пользователя\n\nДля получения истории необходима авторизация',
    request=None,
    responses={
        status.HTTP_200_OK: RentalSerializer(many=True),
        status.HTTP_404_NOT_FOUND: serializers.NotFoundSchemaSerializer,
        status.HTTP_401_UNAUTHORIZED: serializers.UnauthorizedSchemaSerializer
    },
    examples=[
        OpenApiExample(
            name='Пример возвращаемых данных',
            value=[
                {
                    "id": 0,
                    "total_price": "135.15",
                    "start_time": "2024-07-07T16:26:29.043Z",
                    "end_time": "2024-07-07T16:26:29.043Z",
                    "is_paid": True,
                    "bicycle": 0,
                    "user": 0
                },
                {
                    "id": 1,
                    "total_price": "605.44",
                    "start_time": "2024-07-07T16:26:29.043Z",
                    "end_time": "2024-07-07T16:26:29.043Z",
                    "is_paid": True,
                    "bicycle": 2,
                    "user": 1
                },
            ],
        )
    ]
)

rental_create_extend_schema = extend_schema(
    summary='Новая аренда велосипеда',
    description='Создание новой аренды велосипеда\n\nДля аренды необходима авторизация и id арендуемого велосипеда',
    request=serializers.CreateRentalSchemaSerializer,
    responses={
        status.HTTP_201_CREATED: RentalSerializer,
        status.HTTP_401_UNAUTHORIZED: serializers.UnauthorizedSchemaSerializer
    },
    examples=[
        OpenApiExample(
            name='Пример возвращаемых данных',
            value={
                    "id": 0,
                    "total_price": None,
                    "start_time": "2024-07-07T16:26:29.043Z",
                    "end_time": None,
                    "is_paid": False,
                    "bicycle": 0,
                    "user": 0
            },
            response_only=True
        )
    ]
)