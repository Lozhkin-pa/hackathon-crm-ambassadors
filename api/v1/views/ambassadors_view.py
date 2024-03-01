from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
    extend_schema_view,
)
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from ambassadors.models import Ambassador
from api.v1.serializers.ambassadors_serializer import (
    AmbassadorCreateEditSerializer,
    AmbassadorListSerializer,
    AmbassadorRetrieveSerializer,
    ContentSerializer,
)
from api.v1.serializers.yandex_form_ambassador_create_serializer import (
    YandexFormAmbassadorCreateSerializer,
)


@extend_schema(tags=["Амбассадоры"])
@extend_schema_view(
    list=extend_schema(
        summary=("Список амбассадоров."),
        description=(
            "<ul><h3>Фильтрация:</h3>"
            "<li>По точному совпадению даты:"
            " <code>./?created=2023-04-25</code> </li>"
            '<li>По дате "старше чем:" '
            "<code>./?created__gte=2023-04-25</code>"
            "  Т.е. даты старше 2023-04-25</li>"
            '<li>По дате "младше чем:" '
            "<code>./?created__lte=2023-04-25</code>"
            "  Т.е. даты младше 2023-04-25</li>"
            "<li>Множественная "
            "фильтрация по дате: <code>./?created__gte=2023-04-25"
            "&created__lte=2024-03-25</code>    "
            "Т.е. дата старше 2023-04-25 и младше 2024-03-25</li>"
            "<li>По id курса."
            " id берется в эндпоинте <code>./dropdowns</code></li></ul>"
            "<br><ul><h3>Поиск:</h3>"
            "<li>Поиск по имени: <code>./?search=Вася</code></li>"
            "<li>Поиск по стране: <code>./?search=Россия</code></li>"
            "<li>Поиск по городу: <code>./?search=Москва</code></li>"
            "<li>Поиск по курсу: <code>./?search=Веб-разработка</code></li>"
            "</ul>"
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

    queryset = Ambassador.objects.select_related("course", "education_goal")
    http_method_names = ("get", "head", "options", "post", "patch")
    filter_backends = (
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )
    search_fields = (
        "name",
        "country",
        "city",
        "telegram",
        "course__title",
    )
    ordering_fields = ("created",)
    filterset_fields = {
        "created": ["exact", "gte", "lte"],
        "course": ["exact"],
        "sex": ["exact"],
        "status": ["exact"],
        "onboarding_status": ["exact"],
        "country": ["exact"],
        "city": ["exact"],
        "content": ["exact"],
    }

    def get_serializer_class(self):
        """Выбор сериализатора в зависимости от типа запроса."""
        if self.action == "retrieve":
            return AmbassadorRetrieveSerializer
        if self.action == "list":
            return AmbassadorListSerializer
        if self.action == "create" and self.request.headers.get("Yandex"):
            return YandexFormAmbassadorCreateSerializer
        return AmbassadorCreateEditSerializer

    @extend_schema(
        summary="Контент одного амбассадора.",
        description=(
            "Контент конкретного амбассадора"
            " с возможностью фильтрации по дате."
        ),
        request=ContentSerializer,
        responses={200: ContentSerializer},
        parameters=[
            OpenApiParameter(
                name="content_after",
                type=OpenApiTypes.DATE,
                description="Дата после",
            ),
            OpenApiParameter(
                name="content_before",
                type=OpenApiTypes.DATE,
                description="Дата до",
            ),
        ],
    )
    @action(
        methods=["get"],
        detail=False,
        url_path="(?P<pk>[^/.]+)/content",
    )
    def content(self, request, pk):
        content_after = request.query_params.get("content_after")
        content_before = request.query_params.get("content_before")
        queryset = Ambassador.objects.get(id=pk).content.all()

        if content_after:
            queryset = queryset.filter(created__gte=content_after)
        if content_before:
            queryset = queryset.filter(created__lte=content_before)

        serializer = ContentSerializer(queryset, many=True)
        return Response(serializer.data)
