from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import decorators, mixins, viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from ambassadors.models import Ambassador
from api.v1.serializers.promos_serializer import (
    AmbassadorPromoArchiveSerializer,
    PromoActiveSerializer,
    PromoActiveUpdateSerializer,
)
from core.choices import PromoStatus


@extend_schema(tags=["Промокоды"])
@extend_schema_view(
    list=extend_schema(
        summary=("Список промокодов амбассадоров."),
        description=(
            "<ul><h3>Фильтрация:</h3>"
            "<li>Фильтрация по дате: <code>./?created_after=2023-04-25"
            "&created_before=2024-03-25</code>    "
            "т.е. дата старше 2023-04-25 и младше 2024-03-25</li>"
            "<li>Фильтрация по статусу амбассадора: "
            "<code>./?status=active</code> "
            "т.е. active(активный)/paused(на паузе)/"
            "not_ambassador(не амбассадор)/pending(уточняется)</li>"
            "<h3>Поиск:</h3>"
            "<li>Поиск по имени: <code>./?search=Вася</code></li>"
            "</ul>"
        ),
    ),
    retrieve=extend_schema(summary="Активный промокод амбассадора."),
    partial_update=extend_schema(
        summary="Редактирование промокода амбассадора.",
    ),
    archive=extend_schema(summary="Список архивных промокодов"),
)
class PromosViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.UpdateModelMixin
):
    """
    Промокоды амбассадоров.
    Фильтрация по статусу амбассадора (/?status=active).
    Фильтр по дате (/?created_after=2024-02-23&created_before=2024-02-26).
    Поиск по имени (/?search=Смирнова).
    Сортировка по дате (/?ordering=-created).
    """

    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ("status",)
    search_fields = ("name",)
    ordering_fields = ("created",)
    ordering = ("created",)
    http_method_names = ("get", "head", "options", "patch")
    serializer_class = PromoActiveSerializer

    def get_queryset(self):
        queryset = Ambassador.objects.filter(promos__status=PromoStatus.ACTIVE)
        created_after = self.request.query_params.get("created_after")
        created_before = self.request.query_params.get("created_before")
        if created_after:
            queryset = queryset.filter(created__gte=created_after)
        if created_before:
            queryset = queryset.filter(created__lte=created_before)
        return queryset

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от типа запроса."""
        if self.action == "list":
            return PromoActiveSerializer
        return PromoActiveUpdateSerializer

    @extend_schema(summary="Архивные промокоды амбассадоров")
    @decorators.action(
        methods=("get",),
        detail=False,
        url_path="archive",
    )
    def get_archive_promos(self, request):
        """
        Архивные промокоды амбассадоров.
        Фильтрация по статусу амбассадора (/?status=active).
        Фильтр по дате (/?created_after=2024-02-23&created_before=2024-02-26).
        Поиск по имени (/?search=Смирнова).
        Сортировка по дате (/?ordering=-created).
        """

        # queryset = Ambassador.objects.filter(
        #     promos__status=PromoStatus.ARCHIVED
        # )
        queryset = Ambassador.objects.all()
        created_after = self.request.query_params.get("created_after")
        created_before = self.request.query_params.get("created_before")
        ambassador_status = self.request.query_params.get("status")
        search = self.request.query_params.get("search")
        ordering = self.request.query_params.get("ordering", "created")
        if search:
            queryset = queryset.filter(name__icontains=f"{search}")
        if ambassador_status:
            queryset = queryset.filter(status=ambassador_status)
        if created_after:
            queryset = queryset.filter(created__gte=created_after)
        if created_before:
            queryset = queryset.filter(created__lte=created_before)
        if ordering:
            queryset = queryset.order_by(f"{ordering}")
        page = self.paginate_queryset(queryset)
        serializer = AmbassadorPromoArchiveSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)
