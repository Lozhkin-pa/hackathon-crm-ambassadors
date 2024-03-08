from django.db import models


class AmbassadorStatus(models.TextChoices):
    """Статусы Амбассадора."""

    ACTIVE = "active", "Активный"
    PAUSED = "paused", "На паузе"
    NOT_AMBASSADOR = "not_ambassador", "Не амбассадор"
    PENDING = "pending", "Уточняется"


class Sex(models.TextChoices):
    """Пол."""

    M = "m", "Мужской"
    W = "w", "Женский"
    UNKNOWN = "Unknown", "Пол не указан"


class ClothingSize(models.TextChoices):
    """Размер одежды."""

    XS = "XS", "XS - Экстра-маленький"
    S = "S", "S - Маленький"
    M = "M", "M - Средний"
    L = "L", "L - Большой"
    XL = "XL", "XL - Очень большой"
    UNKNOWN = "UNKNOWN", "Размер не указан"


class PromoStatus(models.TextChoices):
    """Статус промокода."""

    ACTIVE = "active", "Активный"
    ARCHIVED = "archived", "Архивный"


class MonthChoices(models.TextChoices):
    """Месяцы для дропдаунов."""

    JANUARY = "january", "Январь"
    FEBRUARY = "february", "Февраль"
    MARCH = "march", "Март"
    APRIL = "april", "Апрель"
    MAY = "may", "Май"
    JUNE = "june", "Июнь"
    JULY = "july", "Июль"
    AUGUST = "august", "Август"
    SEPTEMBER = "september", "Сентябрь"
    OCTOBER = "october", "Октябрь"
    NOVEMBER = "november", "Ноябрь"
    DECEMBER = "december", "Декабрь"
