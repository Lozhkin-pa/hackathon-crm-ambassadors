from djoser.views import UserViewSet as UserViewSetFromDjoser
from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema(tags=["Пользователи"])
@extend_schema_view(
    list=extend_schema(
        summary=("Список пользователей."),
    ),
    retrieve=extend_schema(summary="Профиль пользователя"),
    me=extend_schema(summary="Текущий пользователь"),
)
class UserViewSet(UserViewSetFromDjoser):
    """Пользователи."""

    http_method_names = ["get", "head", "options"]
