import uuid

from django.conf import settings
from django.db import models

from core.abstract_models import AbstractTimeModel


class Content(AbstractTimeModel):
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

    class Meta:
        ordering = ("-created",)
        verbose_name = "Контент"
        verbose_name_plural = "Контент"

    def __str__(self):
        return self.link
