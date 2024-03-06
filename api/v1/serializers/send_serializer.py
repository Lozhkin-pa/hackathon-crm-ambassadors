from rest_framework import serializers

from ambassadors.models import MerchMiddle


class ListCreateSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        product_data = [MerchMiddle(**item) for item in validated_data]
        return MerchMiddle.objects.bulk_create(product_data)


class SendSerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchMiddle
        fields = "__all__"
        list_serializer_class = ListCreateSerializer

    def validate(self, data):
        if "ambassador" not in data:
            raise serializers.ValidationError(
                {"error": "Добавьте амбассадора."}
            )

        if "merch" not in data:
            raise serializers.ValidationError({"error": "Добавьте мерч."})
        return data


class SendInfoSerializer(serializers.ModelSerializer):
    ambassador = serializers.CharField(source="ambassador.name")
    merch = serializers.CharField(source="merch.title")
    country = serializers.CharField(source="ambassador.country")
    city = serializers.CharField(source="ambassador.city")
    address = serializers.CharField(source="ambassador.address")
    index = serializers.CharField(source="ambassador.index")
    phone = serializers.CharField(source="ambassador.phone")

    class Meta:
        model = MerchMiddle
        fields = (
            "ambassador",
            "merch",
            "created",
            "size",
            "country",
            "city",
            "address",
            "index",
            "phone",
        )
