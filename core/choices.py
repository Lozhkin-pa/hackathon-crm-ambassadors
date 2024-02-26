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
    XS = "xs", "XS - Экстра-маленький"
    S = "s", "S - Маленький"
    M = "m", "M - Средний"
    L = "l", "L - Большой"
    XL = "xl", "XL - Очень большой"
    UNKNOWN = "Unknown", "Размер не указан"


class PromoStatus(models.TextChoices):
    """Статус промокода."""

    ACTIVE = "active", "Активный"
    ARCHIVED = "archived", "Архивный"
