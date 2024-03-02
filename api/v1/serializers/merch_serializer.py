from rest_framework import serializers

from ambassadors.models import Ambassador, MerchMiddle
from api.v1.filters import get_period

GRAND_TOTAL = 0


def calculate_grand_total(date_start, date_finish):
    """Вычисление суммарных затрат на мерч."""
    global GRAND_TOTAL
    queryset = MerchMiddle.objects.filter(
        created__gte=date_start, created__lte=date_finish
    )
    GRAND_TOTAL = sum(
        item.old_price * item.count + item.delivery_cost for item in queryset
    )
    return GRAND_TOTAL


class MerchSerializer(serializers.ModelSerializer):
    """Сериализатор мерча."""

    for i in range(1, 13):
        exec("total_{} = serializers.IntegerField()".format(i))
    total_delivery = serializers.IntegerField()
    total_per_amb = serializers.IntegerField()
    grand_total = serializers.SerializerMethodField()

    class Meta:
        model = Ambassador
        fields = (
            "id",
            *[f"total_{i}" for i in range(1, 13)],
            "total_delivery",
            "total_per_amb",
            "grand_total",
        )

    def get_grand_total(self, _):
        if GRAND_TOTAL:
            return GRAND_TOTAL
        return calculate_grand_total(*get_period(self.context["request"]))
