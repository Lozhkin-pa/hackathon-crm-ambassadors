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

    XS = "XS", "XS"
    S = "S", "S"
    M = "M", "M"
    L = "L", "L"
    XL = "XL", "XL"
    UNKNOWN = "UNKNOWN", "Размер не указан"


class SocksSize(models.TextChoices):
    """Размер носков."""

    S_35 = "35"
    S_36 = "36"
    S_37 = "37"
    S_38 = "38"
    S_39 = "39"
    S_40 = "40"
    S_41 = "41"
    S_42 = "42"
    S_43 = "43"
    S_44 = "44"
    S_45 = "45"
    UNKNOWN = "Размер не указан"


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
