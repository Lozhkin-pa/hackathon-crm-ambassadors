from django.db import transaction
from rest_framework import serializers

from ambassadors.models import Ambassador
from content.models import Content


class ContentSerializer(serializers.ModelSerializer):
    """Список Контента амбассадора на чтение."""

    class Meta:
        model = Content
        fields = [
            "id",
            "link",
            "file",
            "guide",
            "created",
            "updated",
        ]


class LastContentSerializer(serializers.ModelSerializer):
    """Последний контент амбассадора на чтение."""

    link = serializers.SerializerMethodField(read_only=True)
    file = serializers.SerializerMethodField(read_only=True)

    def get_link(self, obj):
        if obj.all().count() > 0:
            content = obj.all().order_by("created")
            return content.last().link

    def get_file(self, obj):
        if obj.all().count() > 0:
            content = obj.all().order_by("created")
            return content.last().file

    class Meta:
        model = Content
        fields = [
            "link",
            "file",
        ]


class ListContentSerializer(serializers.ModelSerializer):
    """Список амбассадоров с контентом на чтение."""

    content = ContentSerializer(read_only=True, many=True)
    content_last = LastContentSerializer(source="content", read_only=True)
    guide_step = serializers.SerializerMethodField(read_only=True)
    content_guide_amount = serializers.SerializerMethodField(read_only=True)

    def get_guide_step(self, obj):
        content_amount = obj.content.filter(guide=True).count()
        if content_amount == 0:
            guide_step = "new"
        elif content_amount < 4:
            guide_step = "in_progress"
        else:
            guide_step = "done"
        return guide_step

    def get_content_guide_amount(self, obj):
        content_amount = obj.content.filter(guide=True).count()
        return content_amount if content_amount <= 4 else 4

    class Meta:
        model = Ambassador
        fields = (
            "name",
            "telegram",
            "guide_step",
            "created",
            "updated",
            "content_guide_amount",
            "content",
            "content_last",
        )


class RetrieveContentSerializer(serializers.ModelSerializer):
    """Единица контента определенного амбассадора на чтение."""

    ambassador = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Content
        fields = [
            "id",
            "link",
            "file",
            "guide",
            "created",
            "updated",
            "ambassador",
        ]


class CreateContentSerializer(serializers.ModelSerializer):
    """Контент амбассадора на запись/редактирование контент-менеджером."""

    class Meta:
        model = Content
        fields = [
            "link",
            "file",
            "guide",
            "created",
            "updated",
            "ambassador",
        ]


class FormsContentSerializer(serializers.ModelSerializer):
    """Контент амбассадора на запись из Яндекс Формы."""

    @transaction.atomic
    def create(self, validated_data):
        telegram = validated_data.pop("telegram")
        _ = validated_data.pop("name")
        guide = validated_data.pop("guide")
        ambassador = Ambassador.objects.filter(telegram=telegram)
        content = Content.objects.create(**validated_data)
        content.ambassador = ambassador
        content.guide = True if guide == "Да" else False
        content.save()
        return content

    class Meta:
        model = Content
        fields = [
            "link",
            "file",
            "guide",
            "created",
            "ambassador",
        ]
