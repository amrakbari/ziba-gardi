from django.db import models
from accounts.models import CustomUser, Address


class StylistProfile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class Store(models.Model):
    stylist = models.ForeignKey(StylistProfile, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)

