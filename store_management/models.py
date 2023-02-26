from datetime import datetime

from django.db import models
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

