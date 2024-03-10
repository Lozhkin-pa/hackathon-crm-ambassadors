from django.utils.timesince import timesince
from drf_spectacular.utils import OpenApiTypes, extend_schema_field
from notifications.models import Notification
from rest_framework import serializers

from ambassadors.models import Ambassador


class NotificationSerializer(serializers.ModelSerializer):
    """Сериализатор уведомлений."""

    actor_content_type = serializers.CharField(
        source="actor.__class__.__name__", read_only=True
    )
    target_object_content_type = serializers.CharField(
        source="target.__class__.__name__", read_only=True
    )
    time_since = serializers.SerializerMethodField()
    actor_object_name = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = (
            "id",
            "verb",
            "unread",
            "actor_object_id",
            "actor_object_name",
            "actor_content_type",
            "target_object_id",
            "target_object_content_type",
            "timestamp",
            "description",
            "time_since",
        )

    @extend_schema_field(OpenApiTypes.STR)
    def get_time_since(self, instance):
        """Человеко-читаемое время с момента создания уведомления."""
        return timesince(instance.timestamp, depth=1)

    def get_actor_object_name(self, instance):
        """Имя амбассадора."""
        ambassador = Ambassador.objects.filter(
            id=instance.actor_object_id
        ).first()
        return ambassador.name


class MarkAllAsReadSerializer(serializers.Serializer):
    """Сериализатор для отметки всех уведомлений как прочитанных."""

    marked_as_read_number = serializers.IntegerField()


class UnseenSerializer(serializers.Serializer):
    """Сериализатор количества непрочитанных уведомлений."""

    unseen = serializers.IntegerField()
