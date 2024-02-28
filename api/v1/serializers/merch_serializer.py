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
    total_per_amb = serializers.IntegerField()

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
            "total_per_amb",
        )
