from django_filters.rest_framework import (
    DateFilter,
    DateFromToRangeFilter,
    FilterSet,
)

from ambassadors.models import Ambassador
from content.models import Content


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
    Фильтр контента по дате и имени амбасадора:
    /content/?ambassador__name=Жукова%20Ольга%20Владимировна
    /content/?created_after=2024-02-23&created_before=2024-02-26
    """
    created = DateFromToRangeFilter()

    class Meta:
        model = Content
        fields = (
            'ambassador__name',
            'created',
        )
