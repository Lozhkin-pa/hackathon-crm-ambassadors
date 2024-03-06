from rest_framework import generics, viewsets

from ambassadors.models import MerchMiddle
from api.v1.serializers.send_serializer import (
    SendInfoSerializer,
    SendSerializer,
)


class SendViewSet(generics.CreateAPIView):
    serializer_class = SendSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True

        return super(SendViewSet, self).get_serializer(*args, **kwargs)


class SendInfoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SendInfoSerializer
    queryset = MerchMiddle.objects.all()
