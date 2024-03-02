from datetime import datetime

from django_filters.rest_framework import DateFilter, FilterSet
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
            case _:
                return queryset

    class Meta:
        model = Ambassador
        fields = (
            "content__created",
            "guide_step",
        )

        
def get_period(request):
    """Получение периода за который необходимо получить информацию о мерче."""

    date_start = request.GET.get("start")
    date_finish = request.GET.get("finish")
    current_year = datetime.now().year

    if not date_start and not date_finish:
        date_start = f"{current_year}-1-1"
        date_finish = f"{current_year}-12-31"
    elif not date_finish:
        date_finish = date_start[:4] + "-12-31"
    elif not date_start:
        date_start = date_finish[:4] + "-1-1"

    date_start = datetime.strptime(date_start, "%Y-%m-%d").date()
    date_finish = datetime.strptime(date_finish, "%Y-%m-%d").date()

    return date_start, date_finish
