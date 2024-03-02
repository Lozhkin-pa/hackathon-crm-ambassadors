from rest_framework import serializers

from ambassadors.models import Ambassador, MerchMiddle
from api.v1.filters import get_period

data = [f"total_{i}" for i in range(1, 13)]


class MerchSerializer(serializers.ModelSerializer):
    for i in range(1, 13):
        exec("total_{} = serializers.IntegerField()".format(i))

    total_delivery = serializers.IntegerField()
    total_per_amb = serializers.IntegerField()
    grand_total = serializers.SerializerMethodField()

    class Meta:
        model = Ambassador
        fields = (
            "id",
            *data,
            "total_delivery",
            "total_per_amb",
            "grand_total",
        )

    def get_grand_total(self, object):
        date_start, date_finish = get_period(self.context["request"])
        queryset = MerchMiddle.objects.filter(
            created__gte=date_start, created__lte=date_finish
        )
        res = 0
        for item in queryset:
            res += item.old_price * item.count + item.delivery_cost
        return res
