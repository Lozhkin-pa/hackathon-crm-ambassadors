from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe

from users.models import ExtendedUser

admin.site.unregister(Group)


@admin.register(ExtendedUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Личная информация",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "username",
                    "img",
                    "image_preview",
                )
            },
        ),
        (
            "Привилегии",
            {
                "fields": (
                    "is_active",
                    "is_superuser",
                )
            },
        ),
    )
    list_display = (
        "email",
        "first_name",
        "last_name",
        "userpic_thumbnail",
    )
    readonly_fields = ("image_preview",)
    search_fields = ("email",)
    ordering = ("-date_joined",)

    @admin.display(description="Аватар")
    def userpic_thumbnail(self, obj: ExtendedUser):
        """Малый аватар в общем списке пользователей."""
        return (
            mark_safe(f'<img src={obj.img.url} width="80">')
            if obj.img
            else None
        )

    @admin.display(description="Текущий аватар")
    def image_preview(self, obj: ExtendedUser):
        """Большой аватар в редактирование пользователя."""
        return (
            mark_safe(f'<img src="{obj.img.url}" width="275">')
            if obj.img
            else "Аватар не загружен."
        )
