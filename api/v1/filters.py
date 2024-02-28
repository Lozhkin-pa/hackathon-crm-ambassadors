from django.db.models import Case, Count, When
from django_filters.rest_framework import (
    CharFilter,
    DateFilter,
    DateFromToRangeFilter,
    FilterSet,
)

from ambassadors.models import Ambassador


class AmbassadorFilter(FilterSet):
    """Фильтр амбассадоров."""

    created__gte = DateFilter(field_name="created", lookup_expr="gte")
    created__lte = DateFilter(field_name="created", lookup_expr="lte")

    # TODO: Сделать фильтрацию контента по времени создания.
    class Meta:
        model = Ambassador
        fields = (
            "course",
            "sex",
            "status",
            "onboarding_status",
            "country",
            "city",
            "created",
        )


class ContentFilter(FilterSet):
    """
    Фильтр контента по дате и статусу амбасадора:
    content/?created_after=2024-02-23&created_before=2024-02-26
    content/?guide_step=new
    """

    created = DateFromToRangeFilter()
    guide_step = CharFilter(method="get_guide_step")

    def get_guide_step(self, queryset, name, value):
        content = Ambassador.objects.all().annotate(
            guide_step=Count(Case(When(content__guide=True, then=1)))
        )
        match value:
            case "new":
                return content.filter(guide_step=0).order_by("-created")
            case "in_progress":
                return content.filter(
                    guide_step__gte=1, guide_step__lte=4
                ).order_by("-created")
            case "done":
                return content.filter(guide_step__gte=4).order_by("-created")

    class Meta:
        model = Ambassador
        fields = (
            "content__created",
            "guide_step",
        )
