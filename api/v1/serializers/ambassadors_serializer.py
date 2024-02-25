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
        fields = "__all__"


class AmbassadorGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = AmbassadorGoal
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class PromoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promo
        fields = "__all__"


class AmbassadorSerializer(serializers.ModelSerializer):
    education_goal = EducationGoalSerializer(many=False, read_only=True)
    course = CourseSerializer(many=False, read_only=True)
    ambassadors_goals = AmbassadorGoalSerializer(many=True, read_only=True)
    promo = PromoSerializer(many=False, read_only=True)

    class Meta:
        model = Ambassador
        fields = "__all__"
