from django.db import models


class AbstractDateTimeModel(models.Model):
    """Абстрактная модель времени."""

    created = models.DateTimeField(
        verbose_name="Дата создания", auto_now_add=True
    )
    updated = models.DateTimeField(
        auto_now=True, verbose_name="Дата последнего изменения"
    )

    class Meta:
        abstract = True


class AbstractDateModel(models.Model):
    """Абстрактная модель даты."""

    created = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    updated = models.DateField(
        auto_now=True, verbose_name="Дата последнего изменения"
    )

    class Meta:
        abstract = True
