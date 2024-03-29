from datetime import datetime

from django.db import models
from django.db.models import Q
from rest_framework import exceptions

from accounts.models import CustomUser, Address


class UserProfile(models.Model):
    STYLIST = 'ST'
    USUAL_USER = 'US'
    PROFILE_ROLE_CHOICES = [
        (STYLIST, 'Stylist'),
        (USUAL_USER, 'Usual'),
    ]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    role = models.CharField(max_length=2, choices=PROFILE_ROLE_CHOICES, default=USUAL_USER)
    birth_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)


class Service(models.Model):
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(default=None, null=True)


class Store(models.Model):
    stylist = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    services = models.ManyToManyField(Service)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(default=None, null=True)


class Appointment(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, null=True, default=None, blank=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, default=None)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    def save(self, *args, **kwargs):
        appointments = Appointment.objects.filter(store=self.store).filter(
            Q(start_datetime__range=(self.start_datetime, self.end_datetime)) |
            Q(end_datetime__range=(self.start_datetime, self.end_datetime)) |
            Q(start_datetime__lt=self.start_datetime, end_datetime__gt=self.end_datetime)
        )
        if not len(appointments):
            super(Appointment, self).save(*args, **kwargs)
        else:
            raise exceptions.ValidationError('time is full')
