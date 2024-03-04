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
