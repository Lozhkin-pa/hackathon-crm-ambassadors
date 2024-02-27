from django.db import models


class AbstractTimeModel(models.Model):
    """Абстрактная модель времени."""

    created = models.DateField(verbose_name="Дата создания", auto_now_add=True)
    updated = models.DateField(
        auto_now=True, verbose_name="Дата последнего изменения"
    )

    class Meta:
        abstract = True
