from rest_framework import serializers

from ambassadors.models import Ambassador


class MerchSerializer(serializers.ModelSerializer):
    total_1 = serializers.IntegerField()
    total_2 = serializers.IntegerField()
    total_3 = serializers.IntegerField()
    total_4 = serializers.IntegerField()
    total_5 = serializers.IntegerField()
    total_6 = serializers.IntegerField()
    total_7 = serializers.IntegerField()
    total_8 = serializers.IntegerField()
    total_9 = serializers.IntegerField()
    total_10 = serializers.IntegerField()
    total_11 = serializers.IntegerField()
    total_12 = serializers.IntegerField()
    total_delivery = serializers.IntegerField()
    grand_total = serializers.IntegerField()

    class Meta:
        model = Ambassador
        fields = (
            "id",
            "total_1",
            "total_2",
            "total_3",
            "total_4",
            "total_5",
            "total_6",
            "total_7",
            "total_8",
            "total_9",
            "total_10",
            "total_11",
            "total_12",
            "total_delivery",
            "grand_total",
        )


#   def get_total (self, object):
#  res = {}
#  for month in range(1,4):
#      amb_merch =
# MerchMiddle.objects.filter(ambassador=object, created__month=month)
#      res[month] = sum(i.old_price for i in amb_merch)
#  res['delivery'] = sum(item.delivery_cost for item in
# MerchMiddle.objects.filter(ambassador=object))
#  res['grand_total'] = sum(res.values())
#  return res
