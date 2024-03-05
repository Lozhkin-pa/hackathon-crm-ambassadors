from rest_framework import serializers

from ambassadors.models import Ambassador, MerchMiddle
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


class MerchLoyaltySerializer(serializers.ModelSerializer):
    """Кол-во мерча, отправленного амбассадору."""

    count = serializers.SerializerMethodField()

    class Meta:
        model = Merch
        fields = ("id", "count")

    def get_count(self, merch):
        ambassador = self.context.get("ambassador")
        sent_merch = MerchMiddle.objects.filter(
            ambassador=ambassador, merch=merch
        )
        if sent_merch.exists():
            return getattr(sent_merch.first(), "count")
        return 0
