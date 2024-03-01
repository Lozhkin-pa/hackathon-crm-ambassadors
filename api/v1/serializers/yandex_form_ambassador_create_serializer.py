from django.db.transaction import atomic
from rest_framework import serializers

from ambassadors.models import (
    Ambassador,
    AmbassadorGoal,
    Course,
    EducationGoal,
    Promo,
)
from core.choices import Sex


class YandexFormAmbassadorCreateSerializer(serializers.ModelSerializer):
    """Создание Амбассадора через Яндекс-форму."""

    sex = serializers.CharField(write_only=True, required=False)
    education_goal = serializers.CharField(write_only=True, required=False)
    custom_goal = serializers.CharField(write_only=True, required=False)
    course = serializers.CharField(write_only=True, required=False)
    ambassador_goals = serializers.CharField(write_only=True, required=False)

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
            "custom_goal",
        )

    @atomic
    def create(self, validated_data):
        """Создание амбассадора."""
        sex = validated_data.get("sex")
        new_promo = validated_data.pop("promo", None)
        education_goal_data = validated_data.pop("education_goal", None)
        ambassador_goals_data = validated_data.pop("ambassador_goals", None)
        custom_goal = validated_data.pop("custom_goal", None)
        course = validated_data.pop("course", None)

        ambassador = Ambassador.objects.create(**validated_data)

        if course:
            exist_course = Course.objects.get(title=course)
            ambassador.course = exist_course
        if new_promo:
            Promo.objects.create(value=new_promo, ambassador=ambassador)
        if ambassador_goals_data:
            try:
                ambassador.ambassador_goals.set(
                    AmbassadorGoal.objects.filter(
                        title__in=ambassador_goals_data.split(", ")
                    )
                )
            except AmbassadorGoal.DoesNotExist:
                pass
        if education_goal_data != "Свой вариант":
            ambassador.education_goal = EducationGoal.objects.get(
                title=education_goal_data
            )
        elif custom_goal:
            ambassador.education_goal = EducationGoal.objects.create(
                title=custom_goal
            )
        if sex:
            if sex == "М":
                ambassador.sex = Sex.M
            elif sex == "Ж":
                ambassador.sex = Sex.W
        ambassador.yandex_form = True
        ambassador.save()
        return ambassador
