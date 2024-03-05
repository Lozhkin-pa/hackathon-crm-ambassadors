from django.contrib import admin

from merch.models import Merch


@admin.register(Merch)
class MerchAdmin(admin.ModelAdmin):
    """Панель администратора для Мерча."""

    list_display = (
        "id",
        "title",
        "article",
        "price",
        "created",
    )
    search_fields = ("title", "article")
    ordering = ("-updated",)
