import re

from django.contrib import admin
from django.utils.html import format_html

from ambassadors.models import (
    Ambassador,
    AmbassadorGoal,
    Course,
    EducationGoal,
    MerchMiddle,
    Promo,
)
from content.models import Content


class PromoInline(admin.TabularInline):
    """Добавление промокодов при редактирование амбассадора."""

    model = Promo
    extra = 1


class MerchMiddleInline(admin.TabularInline):
    """Добавление отправленного мерча при редактирование амбассадора."""

    model = MerchMiddle
    extra = 1


class ContentInline(admin.TabularInline):
    """Добавление контента при редактировании амбассадора."""

    model = Content
    extra = 1


@admin.register(Ambassador)
class AmbassadorAdmin(admin.ModelAdmin):
    """Панель администратора для модели Амбассадор."""

    list_display = (
        "name",
        "link_telegram",
        "link_email",
        "status",
        "onboarding_status",
        "sex",
        "city",
    )
    search_fields = (
        "telegram",
        "name",
        "country",
        "city",
        "address",
        "index",
        "email",
        "phone",
    )
    list_filter = (
        "sex",
        "status",
        "city",
    )
    ordering = ("-updated",)
    date_hierarchy = "updated"
    inlines = (
        PromoInline,
        ContentInline,
        MerchMiddleInline,
    )

    @admin.display(description="Телеграм")
    def link_telegram(self, obj):
        """Прямая ссылка на телеграм."""
        if hasattr(obj, "telegram") and obj.telegram is not None:
            if re.match(r"\w+$", obj.telegram):
                return format_html(
                    f'<a href="https://t.me/{obj.telegram}">{obj.telegram}</a>'
                )
            elif re.match(r"https://t\.me/\w+", obj.telegram):
                return format_html(
                    f'<a href="{obj.telegram}">{obj.telegram}</a>'
                )
            else:
                return obj.telegram

    @admin.display(description="email")
    def link_email(self, obj):
        """Прямая ссылка на email."""
        if hasattr(obj, "email") and obj.email is not None:
            return format_html(f'<a href="mailto:{obj.email}">{obj.email}</a>')


@admin.register(EducationGoal)
class EducationGoalAdmin(admin.ModelAdmin):
    """Панель администратора для модели Цель обучения в ЯП."""

    list_display = ("title", "created", "updated")
    search_fields = ("title",)
    ordering = ("-updated",)


@admin.register(AmbassadorGoal)
class AmbassadorGoalAdmin(admin.ModelAdmin):
    """Панель администратора для модели Цель амбассадорства."""

    list_display = ("title", "created", "updated")
    search_fields = ("title",)
    ordering = ("-updated",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Панель администратора для модели Курс Яндекс Практикума."""

    list_display = ("title", "created", "updated")
    search_fields = ("title",)
    ordering = ("-updated",)


@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    """Панель администратора для модели Курс Яндекс Практикума."""

    list_display = ("value", "ambassador", "status", "created", "updated")
    search_fields = ("value",)
    list_filter = ("status",)
    ordering = ("-updated",)


@admin.register(MerchMiddle)
class MerchMiddleAdmin(admin.ModelAdmin):
    """Панель администратора для Мерча амбассадора."""

    list_display = (
        "merch",
        "ambassador",
        "size",
        "delivery_cost",
        "count",
        "created",
    )
    search_fields = ("merch", "ambassador")
    list_filter = ("merch",)
    ordering = ("-updated",)
