import uuid

from django.conf import settings
from django.db import models

from core.abstract_models import AbstractTimeModel
from core.choices import AmbassadorStatus, ClothingSize, PromoStatus, Sex
from merch.models import Merch


class Ambassador(AbstractTimeModel):
    """Амбассадоры."""

    id = models.UUIDField(
        "Уникальный идентификатор",
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    telegram = models.CharField(
        "Ник в телеграм",
        max_length=settings.NAME_LENGTH,
        null=True,
        blank=True,
    )
    name = models.CharField(
        "ФИО", max_length=settings.NAME_LENGTH, null=True, blank=True
    )
    status = models.CharField(
        "Статус амбассадора",
        max_length=settings.STATUS_LENGTH,
        choices=AmbassadorStatus.choices,
        default=AmbassadorStatus.ACTIVE,
    )
    onboarding_status = models.BooleanField("Статус онбординга", default=False)
    sex = models.CharField(
        "Пол амбассадора",
        choices=Sex.choices,
        default=Sex.UNKNOWN,
        max_length=settings.STATUS_LENGTH,
    )
    country = models.CharField(
        "Страна", max_length=settings.NAME_LENGTH, null=True, blank=True
    )
    city = models.CharField(
        "Город", max_length=settings.NAME_LENGTH, null=True, blank=True
    )
    address = models.CharField(
        "Адрес", max_length=settings.NAME_LENGTH, null=True, blank=True
    )
    index = models.CharField(
        "Индекс", max_length=settings.NAME_LENGTH, null=True, blank=True
    )
    email = models.CharField(
        "Email", max_length=settings.NAME_LENGTH, null=True, blank=True
    )
    phone = models.CharField(
        "Телефон", max_length=settings.NAME_LENGTH, null=True, blank=True
    )
    current_work = models.CharField(
        "Текущее место работы",
        max_length=settings.NAME_LENGTH,
        null=True,
        blank=True,
    )
    education = models.CharField(
        "Образование", max_length=settings.NAME_LENGTH, null=True, blank=True
    )
    blog_link = models.CharField(
        "Ссылка на блог",
        max_length=settings.NAME_LENGTH,
        null=True,
        blank=True,
    )
    clothing_size = models.CharField(
        "Размер одежды",
        choices=ClothingSize.choices,
        default=ClothingSize.UNKNOWN,
        max_length=settings.NAME_LENGTH,
    )
    foot_size = models.CharField(
        "Размер ноги", max_length=settings.NAME_LENGTH, null=True, blank=True
    )
    comment = models.CharField(
        "Комментарий", max_length=settings.NAME_LENGTH, null=True, blank=True
    )
    education_goal = models.ForeignKey(
        "EducationGoal",
        related_name="ambassadors",
        verbose_name="Цель обучения в ЯП",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    ambassador_goals = models.ManyToManyField(
        "AmbassadorGoal",
        verbose_name="Цели амбассадорства",
        related_name="ambassador",
    )
    course = models.ForeignKey(
        "Course",
        verbose_name="Пройденный курс ЯП",
        related_name="ambassadors",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    merch = models.ManyToManyField(
        Merch,
        through="MerchMiddle",
        verbose_name="Мерч",
        related_name="ambassador",
    )
    # TODO: Раскомментировать и дописать после создания этих моделей.
    # content = models.ForeignKey(
    #     "Content",
    #     verbose_name="Контент амбассадора",
    #     related_name="ambassador",
    # )

    class Meta:
        ordering = ("-created",)
        verbose_name = "Амбассадор"
        verbose_name_plural = "Амбассадоры"

    def __str__(self):
        return self.name


class EducationGoal(AbstractTimeModel):
    """Цель обучения в Яндекс Практикуме."""

    title = models.CharField(
        "Цель обучения в ЯП", max_length=settings.NAME_LENGTH
    )

    class Meta:
        verbose_name = "Цель обучения в ЯП"
        verbose_name_plural = "Цели обучения в ЯП"

    def __str__(self):
        return self.title


class AmbassadorGoal(AbstractTimeModel):
    """Цель амбассадорства."""

    title = models.CharField(
        "Цель амбассадорства", max_length=settings.NAME_LENGTH
    )

    class Meta:
        verbose_name = "Цель амбассадорства"
        verbose_name_plural = "Цели амбассадорства"

    def __str__(self):
        return self.title


class Course(AbstractTimeModel):
    """Курс Яндекс Практикума."""

    title = models.CharField("Название курса", max_length=settings.NAME_LENGTH)

    class Meta:
        verbose_name = "Курс Яндекс Практикума"
        verbose_name_plural = "Курсы Яндекс Практикума"

    def __str__(self):
        return self.title


class Promo(AbstractTimeModel):
    """Промокод."""

    value = models.CharField("Промокод", max_length=settings.NAME_LENGTH)
    status = models.CharField(
        "Статус",
        choices=PromoStatus.choices,
        default=PromoStatus.ACTIVE,
        max_length=settings.STATUS_LENGTH,
    )
    ambassador = models.ForeignKey(
        "Ambassador",
        verbose_name="Амбассадор",
        related_name="promos",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Промокод"
        verbose_name_plural = "Промокоды"

    def __str__(self):
        return self.value


class MerchMiddle(models.Model):
    """Промежуточная модель между амбассадором и мерч."""

    class Sizes(models.TextChoices):
        XS = "1", "XS"
        S = "2", "S"
        M = "3", "M"
        L = "4", "L"
        XL = "5", "XL"

    ambassador = models.ForeignKey(
        Ambassador, verbose_name="амбассадор", on_delete=models.CASCADE
    )
    merch = models.ForeignKey(
        Merch, verbose_name="мерч", on_delete=models.SET_NULL, null=True
    )
    size = models.CharField("Размер", max_length=1, choices=Sizes.choices)
    delivery_cost = models.IntegerField("Стоимость доставки", null=True)
    count = models.IntegerField("Количество")
    old_price = models.IntegerField("Архивная цена", blank=True, null=True)

    def __str__(self):
        return f"{self.merch}, {self.ambassador}"
