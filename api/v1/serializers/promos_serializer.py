from rest_framework import serializers

from ambassadors.models import Ambassador, Promo
from core.choices import PromoStatus


class PromoSerializer(serializers.ModelSerializer):
    """Список промокодов."""

    class Meta:
        model = Promo
        fields = (
            "id",
            "value",
            "status",
            "created",
            "updated",
        )


class PromoActiveSerializer(serializers.ModelSerializer):
    """Список активных промокодов амбассадоров."""

    promo = serializers.SerializerMethodField()
    course = serializers.StringRelatedField(read_only=True)

    def get_promo(self, obj):
        promo_active = obj.promos.filter(status=PromoStatus.ACTIVE).first()
        serializer = PromoSerializer(promo_active)
        return serializer.data

    def update(self, instance, validated_data):
        new_promo = validated_data.pop("promo", None)
        if new_promo:
            promos = instance.promos.filter(status=PromoStatus.ACTIVE)
            promos.update(status=PromoStatus.ARCHIVED)
            Promo.objects.create(value=new_promo, ambassador=instance)
        return super().update(instance, validated_data)

    def validate_value(self, value):
        """Валидация промокода."""
        if Promo.objects.filter(value=value).exists():
            raise serializers.ValidationError("Такой промокод уже существует!")
        return value

    class Meta:
        model = Ambassador
        fields = (
            "id",
            "name",
            "telegram",
            "course",
            "promo",
            "created",
            "updated",
            "status",
        )


class PromoActiveUpdateSerializer(serializers.ModelSerializer):
    """Обновление активного промокода амбассадора."""

    promo = serializers.CharField(write_only=True, required=False)

    def update(self, instance, validated_data):
        new_promo = validated_data.pop("promo", None)
        if new_promo:
            promos = instance.promos.filter(status=PromoStatus.ACTIVE)
            promos.update(status=PromoStatus.ARCHIVED)
            Promo.objects.create(value=new_promo, ambassador=instance)
        return super().update(instance, validated_data)

    def validate_value(self, value):
        """Валидация промокода."""
        if Promo.objects.filter(value=value).exists():
            raise serializers.ValidationError("Такой промокод уже существует!")
        return value

    class Meta:
        model = Ambassador
        fields = (
            "id",
            "name",
            "telegram",
            "course",
            "promo",
            "created",
            "updated",
            "status",
        )


class AmbassadorPromoArchiveSerializer(serializers.ModelSerializer):
    """Список амбассадоров c архивными промокодами."""

    promos_archive = serializers.SerializerMethodField()
    course = serializers.StringRelatedField(read_only=True)

    def get_promos_archive(self, obj):
        promos_archive = obj.promos.filter(status=PromoStatus.ARCHIVED)
        serializer = PromoSerializer(promos_archive, many=True)
        return serializer.data

    class Meta:
        model = Ambassador
        fields = (
            "id",
            "name",
            "telegram",
            "course",
            "promos_archive",
            "created",
            "updated",
            "status",
        )
