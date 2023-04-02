from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import mixins, viewsets, permissions
from datetime import datetime
import requests

from accounts.models import Address
from accounts.serializers import AddressSerializer


class SoftDeleteMixin:
    def destroy(self, instance):
        instance.deleted_at = datetime.utcnow()
        instance.save()


class ActivateUser(GenericAPIView):
    def get(self, request, uid, token, *args, **kwargs):
        payload = {'uid': uid, 'token': token}

        url = "http://localhost:8001/auth/users/activation/"
        response = requests.post(url, data=payload)

        if response.status_code == 204:
            return Response({}, response.status_code)
        else:
            return Response(response.json())


class CreateRetrieveListDeleteUpdateAddressViewSet(mixins.CreateModelMixin,
                                                   mixins.ListModelMixin,
                                                   mixins.RetrieveModelMixin,
                                                   mixins.UpdateModelMixin,
                                                   SoftDeleteMixin,
                                                   viewsets.GenericViewSet):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user_id=self.request.user.id, deleted_at=None)

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.save()
