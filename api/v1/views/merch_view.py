import openpyxl
import pandas as pd
from django.db.models import F, Q, Sum
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action

from ambassadors.models import Ambassador
from api.v1.filters import get_period
from api.v1.serializers.merch_serializer import MerchSerializer


class MerchViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет мерча."""

    serializer_class = MerchSerializer

    def sum_per_month(self, month, date_start, date_finish):
        """Вычисление суммы, потраченной на мерч амбассадору за месяц."""
        return Sum(
            F("ambassador__old_price") * F("ambassador__count"),
            filter=Q(ambassador__created__month=month)
            & Q(ambassador__created__gte=date_start)
            & Q(ambassador__created__lte=date_finish),
        )

    def sum_per_year(self, date_start, date_finish):
        """Вычисление суммы, потраченной на мерч амбассадору за год."""
        return Sum(
            "ambassador__delivery_cost",
            filter=Q(ambassador__created__gte=date_start)
            & Q(ambassador__created__lte=date_finish),
        )

    def get_queryset(self):
        global date_start, date_finish
        date_start, date_finish = get_period(self.request)

        queryset = Ambassador.objects.all().annotate(
            total_delivery=self.sum_per_year(date_start, date_finish),
            total_per_amb=Sum(
                F("ambassador__old_price") * F("ambassador__count"),
                filter=Q(ambassador__created__gte=date_start)
                & Q(ambassador__created__lte=date_finish),
            )
            + self.sum_per_year(date_start, date_finish),
        )

        for month in range(1, 13):
            queryset = queryset.annotate(
                **{
                    f"total_{month}": self.sum_per_month(
                        month, date_start, date_finish
                    )
                }
            )
        return queryset

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
            for i in file_headers[date_start.month - 1 : date_finish.month]
        }
        file_data = {"Имя": []} | file_data
        file_data["Доставка"] = []
        file_data["Сумма"] = []
        for j in range(len(queryset)):
            file_data["Имя"].append(str(queryset[j].name))
            for i in range(date_start.month - 1, date_finish.month):
                file_data[file_headers[i]].append(
                    str(queryset[j].__dict__[f"total_{i+1}"])
                )
            file_data["Доставка"].append(
                str(queryset[j].__dict__["total_delivery"])
            )
            file_data["Сумма"].append(
                str(queryset[j].__dict__["total_per_amb"])
            )

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
