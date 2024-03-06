from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from ambassadors.models import Ambassador
from api.v1.filters import get_period
from api.v1.serializers.ambassadors_serializer import (
    AmbassadorLoyaltySerializer,
)


class LoyaltyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Программа лояльности. Выводит информацию про мерч,
    предоставленный амбассадорам.
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
