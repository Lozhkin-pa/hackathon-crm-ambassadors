from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework import routers

from api.v1.views.ambassadors_view import AmbassadorsViewSet
from api.v1.views.users_view import UserViewSet

v1_router = routers.DefaultRouter()
v1_router.register("ambassadors", AmbassadorsViewSet, basename="ambassadors")
v1_router.register("users", UserViewSet, basename="users")


urlpatterns = [
    path("", include(v1_router.urls)),
    path("", include("djoser.urls.authtoken")),
]

#  ------------------------------------------------------------Spectacular_urls
urlpatterns += [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
