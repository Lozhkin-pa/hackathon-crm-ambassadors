import openpyxl
import pandas as pd
from django.db.models import F, Q, Sum
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import viewsets
from rest_framework.decorators import action

from ambassadors.models import Ambassador, MerchMiddle
from api.v1.filters import get_period
from api.v1.serializers.merch_serializer import MerchBudgetSerializer


class MerchBudgetViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет бюджета мерча."""

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

    @action(detail=False, methods=["get"])
    def download(self, _):
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
                    getattr(queryset[j], f"total_{i+1}")
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
        fname = "media/docs/merch_total.xlsx"
        writer = pd.ExcelWriter(fname)
        with pd.ExcelWriter(fname) as writer:
            df.to_excel(writer, index=False)
        wb = openpyxl.load_workbook(fname)
        wb.save(response)
        return response
