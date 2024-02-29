from django_filters.rest_framework import DateFromToRangeFilter, FilterSet

from ambassadors.models import Ambassador


class AmbassadorFilter(FilterSet):
    """Фильтр амбассадоров."""

    created = DateFromToRangeFilter()

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
            "content",
        )
