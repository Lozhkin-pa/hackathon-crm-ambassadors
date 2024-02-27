from django_filters import rest_framework as filters

from content.models import Content


class ContentFilter(filters.FilterSet):
    created = filters.DateFromToRangeFilter()

    class Meta:
        model = Content
        fields = [
            'ambassador__name',
            'created',
        ]
