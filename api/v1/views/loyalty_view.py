from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from ambassadors.models import Ambassador
from api.v1.filters import get_period
from api.v1.serializers.ambassadors_serializer import (
    AmbassadorLoyaltySerializer,
)


@extend_schema(tags=["Программа лояльности"])
@extend_schema_view(
    list=extend_schema(summary=("Список амбассадоров c отправленным мерчем.")),
    retrieve=extend_schema(summary="Амбассадор c отправленным мерчем."),
)
class LoyaltyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Выводит информацию про мерч, предоставленный амбассадорам.
    Фильтрация по дате /?finish=<date>&start=<date>.
    Поиск по имени /?search=Мария.
    """

    serializer_class = AmbassadorLoyaltySerializer
    http_method_names = ("get",)
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    search_fields = ("name",)
    ordering_fields = ("created",)

    def get_queryset(self):
        self.date_start, self.date_finish = get_period(self.request)
        queryset = Ambassador.objects.filter(
            merch__created__gte=self.date_start,
            merch__created__lte=self.date_finish,
        ).distinct()
        return queryset
