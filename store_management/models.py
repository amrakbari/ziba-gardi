from datetime import datetime

from django.db import models
from django.db.models import Q

from accounts.models import CustomUser, Address


class StylistProfile(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(auto_now=True)


class Store(models.Model):
    stylist = models.ForeignKey(StylistProfile, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(auto_now=True)


class UsualUserProfile(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(auto_now=True)


class Appointment(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    user = models.ForeignKey(UsualUserProfile, on_delete=models.CASCADE, null=True, default=None)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    def save(self, *args, **kwargs):
        try:
            self.objects.get(
                Q(start_datetime__range=(self.start_datetime, self.end_datetime)) |
                Q(end_datetime__range=(self.start_datetime, self.end_datetime)) |
                Q(start_datetime__lt=self.start_datetime, end_datetime__gt=self.end_datetime)
            )
        except Appointment.DoesNotExist:
            super(Appointment, self).save(*args, **kwargs)
