from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import (
    OpenApiParameter,
    extend_schema,
    extend_schema_view,
)
from notifications.models import Notification
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from ambassadors.models import Ambassador
from api.v1.serializers.notifications_serializer import (
    MarkAllAsReadSerializer,
    NotificationSerializer,
    UnseenSerializer,
)


@extend_schema(tags=["Уведомления"])
@extend_schema_view(
    list=extend_schema(
        summary="Список уведомлений.",
        description=(
            "Список уведомлений, общий для всех пользователей CRM. "
            "Первыми в списке идут непрочитанные уведомления."
        ),
        parameters=[
            OpenApiParameter(
                name="search",
                description="Поиск по ФИО амбассадора",
                type=OpenApiTypes.STR,
            ),
            OpenApiParameter(
                name="timestamp__gte",
                type=OpenApiTypes.DATETIME,
                description="Дата старше чем",
            ),
            OpenApiParameter(
                name="timestamp__lte",
                type=OpenApiTypes.DATETIME,
                description="Дата меньше чем",
            ),
            OpenApiParameter(
                name="ordering",
                type=OpenApiTypes.STR,
                description=(
                    "Положительная или отрицательная сортировка по времени"
                    " создания уведомления. Пример: <code>-timestamp</code>"
                ),
            ),
            OpenApiParameter(
                name="unread",
                type=OpenApiTypes.BOOL,
                description=(
                    "<code>?unread=true</code> - непрочитанные уведомления"
                    " <code>?unread=false</code> - прочитанные уведомления"
                ),
            ),
        ],
    ),
    retrieve=extend_schema(
        summary="Одно уведомление.",
    ),
    partial_update=extend_schema(
        summary="Отметить уведомление как прочитанное.",
        description=(
            "Чтобы отметить уведомление как прочитанное, нужно "
            "отправить пустой PATCH на <code>./notifications/<id>/</code>"
        ),
    ),
    mark_all_as_read=extend_schema(
        summary="Отметить все уведомления как прочтенные.",
    ),
    unseen=extend_schema(
        summary="Количество непрочитанных уведомлений.",
    ),
)
class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    http_method_names = ("get", "patch", "head", "options")
    queryset = Notification.objects.order_by("-unread")
    filter_backends = (
        DjangoFilterBackend,
        OrderingFilter,
    )
    ordering_fields = ("timestamp",)
    filterset_fields = {
        "timestamp": ("exact", "lte", "gte"),
        "unread": ("exact",),
    }

    def get_queryset(self):
        """Получение уведомлений с поиском по имени амбассадора."""
        queryset = super().get_queryset()
        name = self.request.query_params.get("search", None)
        if name:
            ambassador = Ambassador.objects.filter(
                name__icontains=name
            ).first()
            if ambassador:
                queryset = queryset.filter(actor_object_id=ambassador.id)
            else:
                queryset = queryset.none()
        return queryset

    def partial_update(self, request, pk):
        """Отметить уведомление как прочитанное."""
        notification = self.get_object()
        notification.mark_as_read()
        serializer = self.get_serializer(notification)
        return Response(serializer.data)

    @action(
        methods=["get"], detail=False, serializer_class=MarkAllAsReadSerializer
    )
    def mark_all_as_read(self, request):
        """Отметить все уведомления как прочтенные."""
        number = Notification.objects.mark_all_as_read()
        serializer = MarkAllAsReadSerializer({"marked_as_read_number": number})
        return Response(serializer.data)

    @action(methods=["get"], detail=False, serializer_class=UnseenSerializer)
    def unseen(self, request):
        """Количество непрочитанных уведомлений."""
        unread_count = Notification.objects.unread().count()
        serializer = UnseenSerializer({"unseen": unread_count})
        return Response(serializer.data)
