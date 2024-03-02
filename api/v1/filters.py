from datetime import datetime

from django_filters.rest_framework import DateFilter, FilterSet

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


def get_period(request):
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
