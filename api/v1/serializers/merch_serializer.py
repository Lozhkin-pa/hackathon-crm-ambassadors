from datetime import datetime

from rest_framework import serializers

from ambassadors.models import Ambassador, MerchMiddle

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

    def period(self):
        date_start = self.context["request"].GET.get("start")
        date_finish = self.context["request"].GET.get("finish")

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

    def get_grand_total(self, object):
        date_start, date_finish = self.period()
        queryset = MerchMiddle.objects.filter(
            created__gte=date_start, created__lte=date_finish
        )
        res = 0
        for item in queryset:
            res += item.old_price * item.count + item.delivery_cost
        return res
