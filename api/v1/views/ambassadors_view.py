from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.viewsets import ModelViewSet

from ambassadors.models import Ambassador
from api.v1.filters import AmbassadorFilter
from api.v1.serializers.ambassadors_serializer import (
    AmbassadorCreateSerializer,
    AmbassadorListSerializer,
    AmbassadorRetrieveSerializer,
)


@extend_schema(tags=["Амбассадоры"])
@extend_schema_view(
    list=extend_schema(
        summary=("Список амбассадоров."),
        description=(
            "<ul><h3>Поддерживается:</h3>"
            "<li> Фильтрация по точному совпадению даты:"
            " <code>./?created=2023-04-25</code> </li>"
            "<li>Фильтрация по дате старше чем: "
            "<code>./?created__gte=2023-04-25</code></li>"
            "Т.е. даты старше 2023-04-25<li>Множественная"
            " фильтрация по дате: <code>./?created__gte=2023-04-25"
            "&created__lte=2024-03-25</code></li>"
            "Т.е. дата старше 2023-04-25 и младше 2024-03-25"
            "<li>Фильтрация по курсу это фильтрация по id курса."
            " id  в эндпоинте <code>./dropdowns</code></li></ul>"
        ),
    ),
    retrieve=extend_schema(summary="Один амбассадор."),
    create=extend_schema(
        summary="Создание амбассадора.",
        description=(
            "<br><ul><h3>Создание амбассадоров:</h3>"
            "<li> В полях с дропдаунами нужно передавать id которое пришло"
            " вместе со значением с <code>./dropdowns</code></li></ul>"
        ),
    ),
    partial_update=extend_schema(
        summary="Редактирование амбассадора.",
    ),
)
class AmbassadorsViewSet(ModelViewSet):
    """Амбассадоры."""

    queryset = Ambassador.objects.all()
    http_method_names = ("get", "head", "options", "post", "patch")
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    filterset_class = AmbassadorFilter
    search_fields = ("name", "country", "city", "course__name", "telegram")
    ordering_fields = ("created",)

    def get_serializer_class(self):
        """Выбор сериализатор в зависимости от типа запроса."""
        if self.action == "retrieve":
            return AmbassadorRetrieveSerializer
        if self.action == "list":
            return AmbassadorListSerializer
        return AmbassadorCreateSerializer
