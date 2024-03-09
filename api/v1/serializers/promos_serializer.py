from rest_framework import serializers

from ambassadors.models import Promo


class PromoSerializer(serializers.ModelSerializer):
    """Список промокодов амбассадоров."""

    name = serializers.CharField(source="ambassador.name")
    telegram = serializers.CharField(source="ambassador.telegram")
    course = serializers.CharField(source="ambassador.course")
    created = serializers.CharField(source="ambassador.created")
    status = serializers.CharField(source="ambassador.status")
    ambassador_id = serializers.CharField(source="ambassador.id")

    def update(self, instance, validated_data):
        instance.value = validated_data.get("value", instance.value)
        instance.save()
        return instance

    def validate_value(self, value):
        """Валидация промокода."""
        if Promo.objects.filter(value=value).exists():
            raise serializers.ValidationError("Такой промокод уже существует!")
        return value

    class Meta:
        model = Promo
        fields = (
            "id",
            "ambassador_id",
            "name",
            "telegram",
            "course",
            "value",
            "created",
            "updated",
            "status",
        )
