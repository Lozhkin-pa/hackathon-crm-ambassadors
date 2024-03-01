from django.utils.timesince import timesince
from drf_spectacular.utils import OpenApiTypes, extend_schema_field
from notifications.models import Notification
from rest_framework import serializers


class NotificationSerializer(serializers.ModelSerializer):
    """Сериализатор уведомлений."""

    actor_content_type = serializers.CharField(
        source="target.__class__.__name__", read_only=True
    )
    time_since = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = (
            "id",
            "verb",
            "unread",
            "actor_object_id",
            "actor_content_type",
            "timestamp",
            "description",
            "time_since",
        )

    @extend_schema_field(OpenApiTypes.STR)
    def get_time_since(self, instance):
        """Человеко-читаемое время с момента создания уведомления."""
        return timesince(instance.timestamp, depth=1)


class MarkAllAsReadSerializer(serializers.Serializer):
    """Сериализатор для отметки всех уведомлений как прочитанных."""

    marked_as_read_number = serializers.IntegerField()


class UnseenSerializer(serializers.Serializer):
    """Сериализатор количества непрочитанных уведомлений."""

    unseen = serializers.IntegerField()
