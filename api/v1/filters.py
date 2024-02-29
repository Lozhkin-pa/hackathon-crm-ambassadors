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
