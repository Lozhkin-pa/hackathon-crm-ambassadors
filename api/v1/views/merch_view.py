from datetime import datetime

import openpyxl
import pandas as pd
from django.db.models import F, Q, Sum
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action

from ambassadors.models import Ambassador
from api.v1.serializers.merch_serializer import MerchSerializer


class MerchViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = MerchSerializer
    current_year = datetime.now().year

    def sum_per_month(self, month, date_start, date_finish):
        return Sum(
            F("ambassador__old_price") * F("ambassador__count"),
            filter=Q(ambassador__created__month=month)
            & Q(ambassador__created__gte=date_start)
            & Q(ambassador__created__lte=date_finish),
        )

    def sum_per_year(self, date_start, date_finish):
        return Sum(
            "ambassador__delivery_cost",
            filter=Q(ambassador__created__gte=date_start)
            & Q(ambassador__created__lte=date_finish),
        )

    def get_period(self):
        date_start = self.request.GET.get("start")
        date_finish = self.request.GET.get("finish")

        if not date_start and not date_finish:
            date_start = f"{type(self).current_year}-1-1"
            date_finish = f"{type(self).current_year}-12-31"
        elif not date_finish:
            date_finish = date_start[:4] + "-12-31"
        elif not date_start:
            date_start = date_finish[:4] + "-1-1"

        date_start = datetime.strptime(date_start, "%Y-%m-%d").date()
        date_finish = datetime.strptime(date_finish, "%Y-%m-%d").date()
        return date_start, date_finish

    def get_queryset(self):
        date_start, date_finish = self.get_period()

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
    def download(self, request, **kwargs):
        file_headers = [
            "Имя",
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
            "Доставка",
            "Сумма",
        ]
        file_data = {i: [] for i in file_headers}
        for j in range(len(self.get_queryset())):
            file_data["Имя"].append(str(self.get_queryset()[j].name))
            for i in range(1, 13):
                file_data[file_headers[i]].append(
                    str(self.get_queryset()[j].__dict__[f"total_{i}"])
                )
            file_data[file_headers[13]].append(
                str(self.get_queryset()[j].__dict__["total_delivery"])
            )
            file_data[file_headers[14]].append(
                str(self.get_queryset()[j].__dict__["total_per_amb"])
            )
        df = pd.DataFrame(file_data)

        response = HttpResponse(content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = 'attachment;filename="test.xlsx"'
        fname = "test.xlsx"
        writer = pd.ExcelWriter(fname)
        with pd.ExcelWriter(fname) as writer:
            df.to_excel(writer, index=False)

        wb = openpyxl.load_workbook(fname)
        wb.save(response)
        return response


"""    def dispatch(self, request, *args, **kwargs):
            # TODO: Удалить.
            from django.db import connection
            res = super().dispatch(request, *args, **kwargs)
            print("--------------------------------------------------------------")
            print("Запрос:    ", request)
            print("--------------------------------------------------------------")
            print("Количество запросов в БД:  ", len(connection.queries))
            print("--------------------------------------------------------------")
            for q in connection.queries:
                print(">>>>", q["sql"])
            return res  # noqa R504"""
