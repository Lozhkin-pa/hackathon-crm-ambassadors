from rest_framework import serializers

from merch.models import Merch


class MerchSerializer(serializers.ModelSerializer):
    """Варианты мерча."""

    class Meta:
        model = Merch
        fields = ("id", "title", "price")
