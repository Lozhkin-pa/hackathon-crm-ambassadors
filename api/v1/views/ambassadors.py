from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.viewsets import ModelViewSet

from ambassadors.models import Ambassador
from api.v1.serializers.ambassadors_serializer import AmbassadorSerializer


@extend_schema(tags=["Амбассадоры"])
@extend_schema_view(
    list=extend_schema(summary=("Список амбассадоров.")),
    retrieve=extend_schema(summary="Один амбассадор."),
)
class AmbassadorsViewSet(ModelViewSet):
    """Амбассадоры."""

    queryset = Ambassador.objects.all()
    serializer_class = AmbassadorSerializer
    http_method_names = ("get",)
