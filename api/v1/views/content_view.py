from django.db.models import Case, Count, When
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import decorators, status, viewsets
from rest_framework.response import Response

from ambassadors.models import Ambassador
from api.v1.serializers.content_serializer import (
    CreateContentSerializer,
    FormsContentSerializer,
    ListContentSerializer,
    RetrieveContentSerializer,
)
from content.models import Content


@extend_schema(tags=["Контент"])
@extend_schema_view(
    list=extend_schema(
        summary=("Список амбассадоров с контентом."),
        description=(
            "<ul><h3>Фильтрация:</h3>"
            "<li>Фильтрация по дате: <code>./?created__gte=2023-04-25"
            "&created__lte=2024-03-25</code>    "
            "т.е. дата старше 2023-04-25 и младше 2024-03-25</li>"
            "<li>Фильтрация по статусу гайда: <code>./?guide_step=new   "
            "т.е. new(новенький)/in_progress(в процессе)/done(выполнено)</li>"
            "<br><ul><h3>Поиск:</h3>"
            "<li>Поиск по имени: <code>./?search=Вася</code></li>"
            "</ul>"
        ),
    ),
    retrieve=extend_schema(summary="Единица контента амбассадора."),
    create=extend_schema(summary="Создание контента."),
    partial_update=extend_schema(
        summary="Редактирование контента амбассадора.",
    ),
    forms=extend_schema(summary="Получение контента из Яндекс Формы"),
)
class ContentViewSet(viewsets.ModelViewSet):
    """Контент амбассадора."""

    queryset = Content.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return RetrieveContentSerializer
        if self.action in ["create", "partial_update", "delete"]:
            return CreateContentSerializer

    def list(self, request):
        guide_step = self.request.query_params.get("guide_step")
        created_after = self.request.query_params.get("created_after")
        created_before = self.request.query_params.get("created_before")
        queryset = Ambassador.objects.all().annotate(
            guide_step=Count(Case(When(content__guide=True, then=1)))
        )
        # Фильтр по дате /?created_after=2024-02-23&created_before=2024-02-26:
        if created_after and created_before is not None:
            queryset = queryset.filter(
                created__range=(created_after, created_before)
            )
        serializer_new = ListContentSerializer(
            queryset.filter(guide_step=0).order_by("-created"), many=True
        )
        serializer_in_prog = ListContentSerializer(
            queryset.filter(guide_step__gte=1, guide_step__lte=4).order_by(
                "-created"
            ),
            many=True,
        )
        serializer_done = ListContentSerializer(
            queryset.filter(guide_step__gte=4).order_by("-created"), many=True
        )
        # Фильтр по статусу гайда (/?guide_step=new):
        match guide_step:
            case "new":
                data = serializer_new.data
            case "in_progress":
                data = serializer_in_prog.data
            case "done":
                data = serializer_done.data
            case _:
                data = {
                    "new": serializer_new.data,
                    "in_progress": serializer_in_prog.data,
                    "done": serializer_done.data,
                }
        # Поиск по имени (/?name=Смирнова):
        name = self.request.query_params.get("name")
        if name is not None:
            data = ListContentSerializer(
                queryset.filter(name__icontains=name).order_by("-created"),
                many=True,
            ).data
        return Response(data)

    @decorators.action(
        methods=("post",),
        detail=False,
        url_name="forms",
    )
    def get_content_from_forms(self, request):
        """Получение контента амбассадора из Яндекс Формы."""

        if Ambassador.objects.filter(
            telegram=request.data.get("telegram")
        ).exists():
            serializer = FormsContentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
