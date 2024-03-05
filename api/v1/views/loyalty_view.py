from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from ambassadors.models import Ambassador
from api.v1.filters import AmbassadorFilter
from api.v1.serializers.ambassadors_serializer import (
    AmbassadorLoyaltySerializer,
)


class LoyaltyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Программа лояльности. Выводит информацию про мерч,
    предоставленный амбассадорам.
    """

    queryset = Ambassador.objects.all()
    serializer_class = AmbassadorLoyaltySerializer
    http_method_names = ("get",)
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    filterset_class = AmbassadorFilter
    search_fields = ("name",)
    ordering_fields = ("created",)
