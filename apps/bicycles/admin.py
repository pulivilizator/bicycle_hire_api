from django.contrib import admin

from apps.bicycles.models import Bicycle, Rental


# Register your models here.
@admin.register(Bicycle)
class RentalAdmin(admin.ModelAdmin):
    list_display = ['id', 'available', 'price_per_minute']
    list_filter = ['available', 'price_per_minute']
    ordering = ['available', 'price_per_minute']


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ['bicycle', 'user', 'start_time', 'end_time', 'total_price', 'is_paid']