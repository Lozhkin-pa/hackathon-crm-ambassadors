from rest_framework import serializers

from ambassadors.models import Ambassador
from merch.models import Merch


class MerchBudgetSerializer(serializers.ModelSerializer):
    """Сериализатор мерча."""

    for i in range(1, 13):
        exec(f"total_{i} = serializers.IntegerField()")
    total_delivery = serializers.IntegerField()
    total_per_amb = serializers.IntegerField()

    class Meta:
        model = Ambassador
        fields = (
            "id",
            "name",
            *[f"total_{i}" for i in range(1, 13)],
            "total_delivery",
            "total_per_amb",
        )


class MerchSerializer(serializers.ModelSerializer):
    """Варианты мерча."""

    class Meta:
        model = Merch
        fields = ("id", "title", "price")
