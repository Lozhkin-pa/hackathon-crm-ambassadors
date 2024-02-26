from django.contrib import admin

from .models import Content


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    """Панель администратора для модели Контент."""

    list_display = (
        "id",
        "platform",
        "link",
        "file",
        "guide",
        "created",
    )
    search_fields = (
        "platform",
        "guide",
    )
    list_filter = (
        "platform",
        "guide",
    )
    ordering = ("-created",)
