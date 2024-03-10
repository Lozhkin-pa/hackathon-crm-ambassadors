from rest_framework import serializers

from ambassadors.models import Ambassador


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
