from datetime import datetime

from django.db.models import F, Q, Sum
from rest_framework import viewsets

from ambassadors.models import Ambassador
from api.v1.serializers.merch_serializer import MerchSerializer


class MerchViewSet(viewsets.ReadOnlyModelViewSet):
    #  queryset = Ambassador.objects.all()
    serializer_class = MerchSerializer

    def get_queryset(self):
        current_year = datetime.now().year
        queryset = Ambassador.objects.all().annotate(
            total_1=Sum(
                F("ambassador__old_price") * F("ambassador__count"),
                filter=Q(ambassador__created__month=1)
                & Q(ambassador__created__year=current_year),
            ),
            total_2=Sum(
                F("ambassador__old_price") * F("ambassador__count"),
                filter=Q(ambassador__created__month=2)
                & Q(ambassador__created__year=current_year),
            ),
            total_3=Sum(
                F("ambassador__old_price") * F("ambassador__count"),
                filter=Q(ambassador__created__month=3)
                & Q(ambassador__created__year=current_year),
            ),
            total_4=Sum(
                F("ambassador__old_price") * F("ambassador__count"),
                filter=Q(ambassador__created__month=4)
                & Q(ambassador__created__year=current_year),
            ),
            total_5=Sum(
                F("ambassador__old_price") * F("ambassador__count"),
                filter=Q(ambassador__created__month=5)
                & Q(ambassador__created__year=current_year),
            ),
            total_6=Sum(
                F("ambassador__old_price") * F("ambassador__count"),
                filter=Q(ambassador__created__month=6)
                & Q(ambassador__created__year=current_year),
            ),
            total_7=Sum(
                F("ambassador__old_price") * F("ambassador__count"),
                filter=Q(ambassador__created__month=7)
                & Q(ambassador__created__year=current_year),
            ),
            total_8=Sum(
                F("ambassador__old_price") * F("ambassador__count"),
                filter=Q(ambassador__created__month=8)
                & Q(ambassador__created__year=current_year),
            ),
            total_9=Sum(
                F("ambassador__old_price") * F("ambassador__count"),
                filter=Q(ambassador__created__month=9)
                & Q(ambassador__created__year=current_year),
            ),
            total_10=Sum(
                F("ambassador__old_price") * F("ambassador__count"),
                filter=Q(ambassador__created__month=10)
                & Q(ambassador__created__year=current_year),
            ),
            total_11=Sum(
                F("ambassador__old_price") * F("ambassador__count"),
                filter=Q(ambassador__created__month=11)
                & Q(ambassador__created__year=current_year),
            ),
            total_12=Sum(
                F("ambassador__old_price") * F("ambassador__count"),
                filter=Q(ambassador__created__month=12)
                & Q(ambassador__created__year=current_year),
            ),
            total_delivery=Sum(
                "ambassador__delivery_cost",
                filter=Q(ambassador__created__year=current_year),
            ),
            grand_total=Sum(
                F("ambassador__old_price") * F("ambassador__count"),
                filter=Q(ambassador__created__year=current_year),
            ),
        )
        return queryset
