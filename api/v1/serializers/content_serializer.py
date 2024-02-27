from django.db import transaction
from rest_framework import serializers

from ambassadors.models import Ambassador
from content.models import Content


class ListContentSerializer(serializers.ModelSerializer):
    """Список Контента амбассадоров на чтение."""

    ambassador = serializers.StringRelatedField(read_only=True)
    telegram = serializers.CharField(
        source='ambassador.telegram',
        read_only=True
    )
    guide_step = serializers.SerializerMethodField(read_only=True)
    content_amount = serializers.SerializerMethodField(read_only=True)

    def get_guide_step(self, obj):
        content = obj.ambassador.content.filter(guide=True)
        content_amount = content.count()
        if content_amount == 0:
            guide_step = 'new'
        elif content_amount < 4:
            guide_step = 'in_progress'
        else:
            guide_step = 'done'
        return guide_step

    def get_content_amount(self, obj):
        content = obj.ambassador.content.filter(guide=True)
        content_amount = content.count()
        return content_amount if content_amount <= 4 else 4

    class Meta:
        model = Content
        fields = [
            'id',
            'platform',
            'link',
            'file',
            'created',
            'updated',
            'ambassador',
            'telegram',
            'guide_step',
            'content_amount'
        ]


class RetrieveContentSerializer(serializers.ModelSerializer):
    """Контент определенного амбассадора на чтение."""

    ambassador = serializers.StringRelatedField(read_only=True)
    content_amount = serializers.SerializerMethodField(read_only=True)

    def get_content_amount(self, obj):
        content = obj.ambassador.content.filter(guide=True)
        content_amount = content.count()
        return content_amount if content_amount <= 4 else 4

    class Meta:
        model = Content
        fields = [
            'id',
            'platform',
            'link',
            'file',
            'guide',
            'created',
            'updated',
            'ambassador',
            'content_amount'
        ]


class CreateContentSerializer(serializers.ModelSerializer):
    """Контент амбассадора на запись/редактирование контент-менеджером."""

    class Meta:
        model = Content
        fields = [
            # 'platform',
            'link',
            'file',
            'guide',
            'created',
            'updated',
            'ambassador',
        ]


class FormsContentSerializer(serializers.ModelSerializer):
    """Контент амбассадора на запись из Яндекс Формы."""

    @transaction.atomic
    def create(self, validated_data):
        telegram = validated_data.pop('telegram')
        _ = validated_data.pop('name')
        guide = validated_data.pop('guide')
        ambassador = Ambassador.objects.filter(telegram=telegram)
        content = Content.objects.create(**validated_data)
        content.ambassador = ambassador
        content.guide = True if guide == 'Да' else False
        content.save()
        return content

    class Meta:
        model = Content
        fields = [
            # 'platform',
            'link',
            'file',
            'guide',
            'created',
            'ambassador',
        ]
