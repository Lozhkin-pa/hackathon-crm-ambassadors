from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import generics

from api.v1.serializers.send_serializer import SendSerializer


@extend_schema(tags=["Отправить (мерч)"])
@extend_schema_view(
    create=extend_schema(summary="Кнопка 'Отправить'."),
)
class SendViewSet(generics.CreateAPIView):
    """Отправить мерч амбассадору."""

    serializer_class = SendSerializer

    def get_serializer(self, *args, **kwargs):
        if isinstance(kwargs.get("data", {}), list):
            kwargs["many"] = True

        return super(SendViewSet, self).get_serializer(*args, **kwargs)
