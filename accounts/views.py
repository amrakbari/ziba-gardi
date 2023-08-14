import os

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import mixins, viewsets, permissions
from datetime import datetime
import requests

from accounts.models import Address, Neighbourhood
from accounts.serializers import AddressSerializer, NeighbourhoodSerializer


class ActivateUser(GenericAPIView):
    def get(self, request, uid, token, *args, **kwargs):
        payload = {'uid': uid, 'token': token}

        url = f"http://{os.environ.get('HOST')}:8000/auth/users/activation/"
        response = requests.post(url, data=payload)

        if response.status_code == 204:
            return Response({}, response.status_code)
        else:
            return Response(response.json())


class CreateRetrieveListDeleteUpdateAddressViewSet(mixins.CreateModelMixin,
                                                   mixins.ListModelMixin,
                                                   mixins.RetrieveModelMixin,
                                                   mixins.UpdateModelMixin,
                                                   mixins.DestroyModelMixin,
                                                   viewsets.GenericViewSet):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user_id=self.request.user.id, deleted_at=None)

    def get_object(self):
        id_ = self.kwargs.get('pk')
        return Address.objects.get(id=id_)

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.save()

    def perform_destroy(self, instance):
        instance.deleted_at = datetime.utcnow()
        instance.save()


class ListNeighbourhoodViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = NeighbourhoodSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Neighbourhood.objects.all()