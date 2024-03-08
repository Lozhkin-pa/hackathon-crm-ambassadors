from django.db.transaction import atomic
from rest_framework import serializers

from ambassadors.models import (
    Ambassador,
    AmbassadorGoal,
    Course,
    EducationGoal,
    MerchMiddle,
    Promo,
)
from api.v1.serializers.merch_serializer import MerchLoyaltySerializer
from content.models import Content
from core.choices import PromoStatus
from merch.models import Merch


class EducationGoalSerializer(serializers.ModelSerializer):
    """Цели обучения."""

    class Meta:
        model = EducationGoal
        fields = ("id", "title")


class AmbassadorGoalSerializer(serializers.ModelSerializer):
    """Целей амбассадора."""

    class Meta:
        model = AmbassadorGoal
        fields = ("id", "title")


class CourseSerializer(serializers.ModelSerializer):
    """Список курсов."""

    class Meta:
        model = Course
        fields = ("id", "title")


class PromoSerializer(serializers.ModelSerializer):
    """Список промокодов."""

    class Meta:
        model = Promo
        fields = ("id", "value", "status")


class CreatePromoSerializer(serializers.ModelSerializer):
    """Создание промокода."""

    class Meta:
        model = Promo
        fields = ("value",)


class ContentSerializer(serializers.ModelSerializer):
    """Список контента."""

    class Meta:
        model = Content
        fields = (
            "id",
            "link",
            "file",
            "created",
            "updated",
        )


class AmbassadorRetrieveSerializer(serializers.ModelSerializer):
    """Чтение одного Амбассадора."""

    education_goal = EducationGoalSerializer(many=False, read_only=True)
    course = CourseSerializer(many=False, read_only=True)
    ambassador_goals = AmbassadorGoalSerializer(many=True, read_only=True)
    promo = PromoSerializer(many=True, read_only=True)
    guide_content = serializers.SerializerMethodField(read_only=True)
    content = ContentSerializer(many=True, read_only=True)

    class Meta:
        model = Ambassador
        fields = (
            "id",
            "telegram",
            "name",
            "status",
            "onboarding_status",
            "sex",
            "education_goal",
            "country",
            "city",
            "address",
            "index",
            "email",
            "phone",
            "current_work",
            "education",
            "blog_link",
            "clothing_size",
            "foot_size",
            "comment",
            "ambassador_goals",
            "course",
            "created",
            "updated",
            "promo",
            "guide_content",
            "content",
        )

    def get_guide_content(self, ambassador):
        """Возвращает количество контента в рамках гайда."""
        content_amount = ambassador.content.filter(guide=True).count()
        return content_amount if content_amount <= 4 else "4"


class AmbassadorListSerializer(serializers.ModelSerializer):
    """Список амбассадоров."""

    course = CourseSerializer(many=False, read_only=True)

    class Meta:
        model = Ambassador
        fields = (
            "id",
            "name",
            "sex",
            "created",
            "status",
            "country",
            "city",
            "course",
            "onboarding_status",
        )


class AmbassadorCreateEditSerializer(serializers.ModelSerializer):
    """Создание Амбассадора."""

    promo = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Ambassador
        fields = (
            "id",
            "telegram",
            "name",
            "status",
            "onboarding_status",
            "sex",
            "country",
            "city",
            "address",
            "index",
            "email",
            "phone",
            "current_work",
            "education",
            "blog_link",
            "clothing_size",
            "foot_size",
            "comment",
            "course",
            "created",
            "updated",
            "education_goal",
            "ambassador_goals",
            "promo",
        )

    @atomic
    def create(self, validated_data):
        """Создание амбассадора."""
        new_promo = validated_data.pop("promo", None)
        education_goal_data = validated_data.pop("education_goal", None)
        ambassador_goals_data = validated_data.pop("ambassador_goals", None)
        ambassador = Ambassador.objects.create(**validated_data)
        if new_promo:
            Promo.objects.create(value=new_promo, ambassador=ambassador)
        if education_goal_data:
            ambassador.education_goal = education_goal_data
        if ambassador_goals_data:
            ambassador.ambassador_goals.set(ambassador_goals_data)
        ambassador.save()
        return ambassador

    @atomic
    def update(self, instance, validated_data):
        """Изменение амбассадора."""
        new_promo = validated_data.pop("promo", None)

        if new_promo:
            # Старый промокод уходит в архив.
            promos = instance.promos.filter(status=PromoStatus.ACTIVE)
            promos.update(status=PromoStatus.ARCHIVED)
            # Создается новый промокод.
            Promo.objects.create(value=new_promo, ambassador=instance)
        return super().update(instance, validated_data)

    def validate_promo(self, value):
        """Валидация промокода."""
        if Promo.objects.filter(value=value).exists():
            raise serializers.ValidationError("Промокод уже существует.")
        return value


class AmbassadorLoyaltySerializer(serializers.ModelSerializer):
    """Отправленный амбассадору мерч."""

    merch = serializers.SerializerMethodField()
    dispatch_date = serializers.SerializerMethodField()
    course = serializers.CharField(source="course.title")

    class Meta:
        model = Ambassador
        fields = ("id", "name", "course", "merch", "dispatch_date")

    def get_merch(self, ambassador):
        merch = Merch.objects.all().order_by("id")
        return MerchLoyaltySerializer(
            merch, many=True, context={"ambassador": ambassador}
        ).data

    def get_dispatch_date(self, ambassador):
        queryset = MerchMiddle.objects.filter(ambassador=ambassador)
        if queryset.count() >= 1:
            return queryset.latest("created").created
