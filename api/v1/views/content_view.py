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
            "<li>Фильтрация по дате: <code>./?created_after=2023-04-25"
            "&created_before=2024-03-25</code>   "
            "т.е. дата старше 2023-04-25 и младше 2024-03-25</li>"
            "<li>Фильтрация по статусу гайда: <code>./?guide_step=new</code> "
            "т.е. new(новенький)/in_progress(в процессе)/done(выполнено)</li>"
            "<h3>Поиск:</h3>"
            "<li>Поиск по имени: <code>./?search=Вася</code></li>"
            "</ul>"
        ),
    ),
    retrieve=extend_schema(summary="Единица контента амбассадора."),
    create=extend_schema(summary="Создание контента."),
    partial_update=extend_schema(
        summary="Редактирование контента амбассадора.",
    ),
)
class ContentViewSet(viewsets.ModelViewSet):
    """Контент амбассадора."""

    queryset = Content.objects.all()
    http_method_names = ("get", "head", "options", "post", "patch")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return RetrieveContentSerializer
        if self.action in ["create", "partial_update", "delete"]:
            return CreateContentSerializer

    def list(self, request):
        """
        Получение списка амбассадоров с контентом.
        Фильтрация по статусу гайда (/?guide_step=new).
        Фильтр по дате (/?created_after=2024-02-23&created_before=2024-02-26).
        Поиск по имени (/?search=Смирнова).
        """
        guide_step = self.request.query_params.get("guide_step")
        created_after = self.request.query_params.get("created_after")
        created_before = self.request.query_params.get("created_before")
        search = self.request.query_params.get("search")
        queryset = Ambassador.objects.all().annotate(
            guide_step=Count(Case(When(content__guide=True, then=1)))
        )
        # Поиск по имени:
        if search:
            queryset = queryset.filter(name__icontains=search)
        # Фильтрация по дате:
        if created_after:
            queryset = queryset.filter(created__gte=created_after)
        if created_before:
            queryset = queryset.filter(created__lte=created_before)
        # Фильтрация по статусу гайда:
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
        return Response(data)

    @extend_schema(summary="Получение контента из Яндекс Формы")
    @decorators.action(
        methods=("post",),
        detail=False,
        url_path="forms",
    )
    def get_content_from_forms(self, request):
        """Получение контента амбассадора из Яндекс Формы."""
        telegram = request.data.get("telegram")
        guide_check = request.data.pop("guide")
        if Ambassador.objects.filter(telegram=telegram).exists():
            ambassador = Ambassador.objects.filter(telegram=telegram).first()
            request.data["ambassador"] = ambassador.id
            request.data["guide"] = True if guide_check == "Да" else False
            serializer = FormsContentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
