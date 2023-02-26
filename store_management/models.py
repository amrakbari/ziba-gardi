from django.db import models
from accounts.models import CustomUser, Address


class StylistProfile(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


# Create your models here.
