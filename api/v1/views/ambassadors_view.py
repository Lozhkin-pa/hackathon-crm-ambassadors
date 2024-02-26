from django_filters.rest_framework import (
    DateFilter,
    DjangoFilterBackend,
    FilterSet,
)
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from ambassadors.models import Ambassador
from api.v1.serializers.ambassadors_serializer import (
    AmbassadorListSerializer,
    AmbassadorRetrieveSerializer,
)


class EventFilter(FilterSet):
    created_gte = DateFilter(field_name="created", lookup_expr="gte")

    class Meta:
        model = Ambassador
        fields = (
            "created",
            "created_gte",
        )


@extend_schema(tags=["Амбассадоры"])
@extend_schema_view(
    list=extend_schema(summary=("Список амбассадоров.")),
    retrieve=extend_schema(summary="Один амбассадор."),
)
class AmbassadorsViewSet(ModelViewSet):
    """Амбассадоры."""

    queryset = Ambassador.objects.all()
    serializer_class = AmbassadorRetrieveSerializer
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
    )
    # filterset_fields = (
    #     "course",
    #     "sex",
    #     "status",
    #     "onboarding_status",
    #     "country",
    #     "city",
    #     "created",
    # )
    filter_class = EventFilter
    search_fields = ("name",)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return AmbassadorRetrieveSerializer
        if self.action == "list":
            return AmbassadorListSerializer
        # TODO:
        #   - Сделать реализацию для POST и PATCH
        return super().get_serializer_class()
