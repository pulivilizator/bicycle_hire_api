from rest_framework.routers import DefaultRouter

from . import views

app_name = 'rentals'

router = DefaultRouter()
router.register('bicycles', views.BicycleViewSet, basename='bicycle')
router.register('rentals', views.RentalViewSet, basename='rental')

