from rest_framework import serializers

from ambassadors.models import (
    Ambassador,
    AmbassadorGoal,
    Course,
    EducationGoal,
    Promo,
)


class EducationGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationGoal
        fields = ("id", "title")


class AmbassadorGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmbassadorGoal
        fields = ("id", "title")


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ("id", "title")


class PromoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promo
        fields = "__all__"


class AmbassadorRetrieveSerializer(serializers.ModelSerializer):
    """Один Амбассадор."""

    education_goal = EducationGoalSerializer(many=False, read_only=True)
    course = CourseSerializer(many=False, read_only=True)
    ambassador_goals = AmbassadorGoalSerializer(many=True, read_only=True)
    promo = PromoSerializer(many=False, read_only=True)

    class Meta:
        model = Ambassador
        fields = "__all__"


class AmbassadorListSerializer(serializers.ModelSerializer):
    """Список амбассадоров."""

    course = CourseSerializer(many=False, read_only=True)

    class Meta:
        model = Ambassador
        fields = (
            "name",
            "sex",
            "created",
            "status",
            "country",
            "city",
            "course",
            "onboarding_status",
        )
