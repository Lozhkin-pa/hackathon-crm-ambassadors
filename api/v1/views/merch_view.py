import openpyxl
import pandas as pd
from django.db.models import F, Q, Sum
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
    extend_schema_view,
)
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from ambassadors.models import Ambassador, MerchMiddle
from api.v1.filters import get_period
from api.v1.serializers.merch_serializer import (
    MerchBudgetSerializer,
    MerchSerializer,
)
from merch.models import Merch


@extend_schema(tags=["Бюджет на мерч"])
@extend_schema_view(
    list=extend_schema(
        summary="Бюджет отправленного мерча.",
        parameters=[
            OpenApiParameter(
                name="start",
                description="Фильтрация по дате начала",
                type=OpenApiTypes.DATE,
            ),
            OpenApiParameter(
                name="finish",
                description="Фильтрация по дате окончания",
                type=OpenApiTypes.DATE,
            ),
        ],
    ),
    download=extend_schema(
        summary="Загрузка exel-файла бюджета отправленного мерча.",
        parameters=[
            OpenApiParameter(
                name="start",
                description="Фильтрация по дате начала",
                type=OpenApiTypes.DATE,
            ),
            OpenApiParameter(
                name="finish",
                description="Фильтрация по дате окончания",
                type=OpenApiTypes.DATE,
            ),
        ],
    ),
)
class MerchBudgetViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Бюджет мерча."""

    serializer_class = MerchBudgetSerializer

    def sum_per_month(self, month, date_start, date_finish):
        """Вычисление суммы, потраченной на мерч амбассадору за месяц."""
        return Sum(
            F("sent_merch__old_price") * F("sent_merch__count"),
            filter=Q(sent_merch__created__month=month)
            & Q(sent_merch__created__gte=date_start)
            & Q(sent_merch__created__lte=date_finish),
        )

    def sum_per_year(self, date_start, date_finish):
        """Вычисление суммы, потраченной на доставку амбассадору за год."""
        return Sum(
            "sent_merch__delivery_cost",
            filter=Q(sent_merch__created__gte=date_start)
            & Q(sent_merch__created__lte=date_finish),
        )

    def get_queryset(self):
        self.date_start, self.date_finish = get_period(self.request)

        queryset = Ambassador.objects.all().annotate(
            total_delivery=self.sum_per_year(
                self.date_start, self.date_finish
            ),
            total_per_amb=Sum(
                F("sent_merch__old_price") * F("sent_merch__count"),
                filter=Q(sent_merch__created__gte=self.date_start)
                & Q(sent_merch__created__lte=self.date_finish),
            )
            + self.sum_per_year(self.date_start, self.date_finish),
        )

        for month in range(1, 13):
            queryset = queryset.annotate(
                **{
                    f"total_{month}": self.sum_per_month(
                        month, self.date_start, self.date_finish
                    )
                }
            )
        return queryset

    @method_decorator(cache_page(60))
    def list(self, request, *args, **kwargs):
        queryset = self.paginate_queryset(self.get_queryset())

        serializer = MerchBudgetSerializer(queryset, many=True)
        grand_total = MerchMiddle.objects.filter(
            created__gte=self.date_start, created__lte=self.date_finish
        ).aggregate(
            grand_total=Sum(F("old_price") * F("count") + F("delivery_cost"))
        )
        return self.get_paginated_response(
            {**grand_total, "data": serializer.data}
        )

    @action(detail=False, methods=["get"], permission_classes=(AllowAny,))
    def download(self, request):
        """Формирование файла отчета по мерчу."""

        file_headers = [
            "Январь",
            "Февраль",
            "Март",
            "Апрель",
            "Май",
            "Июнь",
            "Июль",
            "Август",
            "Сентябрь",
            "Октябрь",
            "Ноябрь",
            "Декабрь",
        ]

        queryset = self.get_queryset()
        file_data = {
            i: []
            for i in file_headers[
                self.date_start.month - 1 : self.date_finish.month
            ]
        }
        file_data = {"Имя": []} | file_data
        file_data["Доставка"] = []
        file_data["Сумма"] = []
        for j in range(len(queryset)):
            file_data["Имя"].append(str(queryset[j].name))
            for i in range(self.date_start.month - 1, self.date_finish.month):
                file_data[file_headers[i]].append(
                    getattr(queryset[j], f"total_{i + 1}")
                )
            file_data["Доставка"].append(
                getattr(queryset[j], "total_delivery")
            )
            file_data["Сумма"].append(getattr(queryset[j], "total_per_amb"))

        df = pd.DataFrame(file_data)
        response = HttpResponse(content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = (
            'attachment;filename="merch_total.xlsx"'
        )
        fname = "merch_total.xlsx"
        writer = pd.ExcelWriter(fname)
        with pd.ExcelWriter(fname) as writer:
            df.to_excel(writer, index=False)
        wb = openpyxl.load_workbook(fname)
        wb.save(response)
        return response


@extend_schema(tags=["Доступный мерч"])
@extend_schema_view(
    list=extend_schema(
        summary=("Список доступного мерча."),
    ),
)
class MerchInfoViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Доступный мерч."""

    serializer_class = MerchSerializer
    queryset = Merch.objects.all().order_by("id")
