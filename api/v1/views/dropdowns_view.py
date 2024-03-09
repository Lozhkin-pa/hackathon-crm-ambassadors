from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, viewsets
from rest_framework.response import Response

from ambassadors.models import (
    Ambassador,
    AmbassadorGoal,
    Course,
    EducationGoal,
)
from api.v1.serializers.ambassadors_serializer import (
    AmbassadorGoalSerializer,
    CourseSerializer,
    EducationGoalSerializer,
)
from api.v1.serializers.merch_serializer import MerchSerializer
from core.choices import (
    AmbassadorStatus,
    ClothingSize,
    MonthChoices,
    PromoStatus,
    Sex,
    SocksSize,
)
from merch.models import Merch


@extend_schema(tags=["Выпадающие списки"])
@extend_schema_view(
    list=extend_schema(
        summary=("Выпадающие списки."),
    ),
    retrieve=extend_schema(
        summary="Отключает метод получения индивидуальных объектов."
    ),
)
class DropdownsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """
    Выпадающие списки для полей:
        "courses",
        "educational_goals",
        "ambassador_goals",
        "merch",
        "countries",
        "cities",
        "ambassador_status",
        "clothing_size",
        "socks_size",
        "promo_status",
        "sex",
        "months".
    """

    def list(self, request):
        courses_queryset = Course.objects.all()
        courses_serializer = CourseSerializer(courses_queryset, many=True)

        educational_goal_queryset = EducationGoal.objects.all()
        educational_goal_serializer = EducationGoalSerializer(
            educational_goal_queryset, many=True
        )

        ambassador_goal_queryset = AmbassadorGoal.objects.all()
        ambassador_goal_serializer = AmbassadorGoalSerializer(
            ambassador_goal_queryset, many=True
        )

        merch_queryset = Merch.objects.all().order_by("id")
        merch_serializer = MerchSerializer(merch_queryset, many=True)

        countries = (
            Ambassador.objects.values_list("country", flat=True)
            .exclude(country=None)
            .distinct()
            .order_by("country")
        )
        cities = (
            Ambassador.objects.values_list("city", flat=True)
            .exclude(city=None)
            .distinct()
            .order_by("city")
        )

        data = {
            "courses": courses_serializer.data,
            "educational_goals": educational_goal_serializer.data,
            "ambassador_goals": ambassador_goal_serializer.data,
            "merch": merch_serializer.data,
            "countries": countries,
            "cities": cities,
            "ambassador_status": {i.value: i.label for i in AmbassadorStatus},
            "clothing_size": {i.value: i.label for i in ClothingSize},
            "socks_size": [i.value for i in SocksSize],
            "promo_status": {i.value: i.label for i in PromoStatus},
            "sex": {i.value: i.label for i in Sex},
            "months": [i.label for i in MonthChoices],
        }
        return Response(data)
