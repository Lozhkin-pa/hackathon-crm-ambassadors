import uuid

from django.conf import settings
from django.db import models

from ambassadors.models import Ambassador
from core.abstract_models import AbstractDateTimeModel


class Content(AbstractDateTimeModel):
    """Контент амбассадора."""

    id = models.UUIDField(
        "Уникальный идентификатор",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    platform = models.CharField(
        "Площадка размещения контента",
        max_length=settings.NAME_LENGTH,
        null=True,
        blank=True,
    )
    link = models.CharField(
        "Ссылка на контент",
        max_length=settings.NAME_LENGTH,
        null=True,
        blank=True,
    )
    file = models.CharField(
        "Ссылка на файл",
        max_length=settings.NAME_LENGTH,
        null=True,
        blank=True,
    )
    guide = models.BooleanField(
        "Контент в рамках гайда",
        default=False,
    )
    ambassador = models.ForeignKey(
        Ambassador,
        verbose_name="Амбассадор",
        related_name="content",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    yandex_form = models.BooleanField(
        "Создан через Яндекс Форму", default=False
    )

    class Meta:
        ordering = ("-created",)
        verbose_name = "Контент"
        verbose_name_plural = "Контент"

    def __str__(self):
        return self.link
