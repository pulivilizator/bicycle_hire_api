from django.db import models


class BicycleAvailableManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(available=True)
