from rest_framework import generics

from api.v1.serializers.send_serializer import SendSerializer


class SendViewSet(generics.CreateAPIView):
    serializer_class = SendSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True

        return super(SendViewSet, self).get_serializer(*args, **kwargs)
