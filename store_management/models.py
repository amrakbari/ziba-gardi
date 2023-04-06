from datetime import datetime

from django.db import models
from django.db.models import Q

from accounts.models import CustomUser, Address


class StylistProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(default=None, null=True)


class Store(models.Model):
    stylist = models.ForeignKey(StylistProfile, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(default=None, null=True)


class UsualUserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(default=None, null=True)


class Service(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    store = models.ManyToManyField(Store)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(default=None, null=True)


class Appointment(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
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
