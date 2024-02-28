from datetime import datetime

from django.db.models import F, Q, Sum
from rest_framework import viewsets

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

    def get_queryset(self):
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

        queryset = Ambassador.objects.all().annotate(
            total_1=self.sum_per_month(1, date_start, date_finish),
            total_2=self.sum_per_month(2, date_start, date_finish),
            total_3=self.sum_per_month(3, date_start, date_finish),
            total_4=self.sum_per_month(4, date_start, date_finish),
            total_5=self.sum_per_month(5, date_start, date_finish),
            total_6=self.sum_per_month(6, date_start, date_finish),
            total_7=self.sum_per_month(7, date_start, date_finish),
            total_8=self.sum_per_month(8, date_start, date_finish),
            total_9=self.sum_per_month(9, date_start, date_finish),
            total_10=self.sum_per_month(10, date_start, date_finish),
            total_11=self.sum_per_month(11, date_start, date_finish),
            total_12=self.sum_per_month(12, date_start, date_finish),
            total_delivery=self.sum_per_year(date_start, date_finish),
            total_per_amb=Sum(
                F("ambassador__old_price") * F("ambassador__count"),
                filter=Q(ambassador__created__gte=date_start)
                & Q(ambassador__created__lte=date_finish),
            )
            + self.sum_per_year(date_start, date_finish),
        )
        return queryset


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
