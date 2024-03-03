from django.conf import settings
from django.db import models

from core.abstract_models import AbstractTimeModel


class Merch(AbstractTimeModel):
    """Модель мерч."""

    title = models.CharField(
        "Название", max_length=settings.NAME_LENGTH, default="", blank=True
    )
    article = models.CharField(
        "Артикул", max_length=settings.NAME_LENGTH, default="", blank=True
    )
    price = models.PositiveIntegerField("Цена", default=0, blank=True)

    class Meta:
        ordering = ("title",)
        verbose_name = "Мерч"
        verbose_name_plural = "Мерч"

    def __str__(self):
        return self.title
