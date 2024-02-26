from django.db import models


class Merch(models.Model):
    """Модель мерч."""

    title = models.TextField("Название")
    article = models.TextField("Артикул")
    price = models.IntegerField("Цена")

    class Meta:
        ordering = ("title",)
        verbose_name = "Мерч"

    def __str__(self):
        return self.title
