from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework import routers

from api.v1.views.ambassadors_view import AmbassadorsViewSet
from api.v1.views.merch_view import MerchViewSet
from api.v1.views.content_view import ContentViewSet
from api.v1.views.dropdowns_view import DropdownsViewSet
from api.v1.views.users_view import UserViewSet

v1_router = routers.DefaultRouter()
v1_router.register("ambassadors", AmbassadorsViewSet, basename="ambassadors")
v1_router.register("dropdowns", DropdownsViewSet, basename="dropdowns")
v1_router.register("content", ContentViewSet, basename="content")
v1_router.register("users", UserViewSet, basename="users")
v1_router.register("merch", MerchViewSet, basename="merch")

urlpatterns = [
    path("", include(v1_router.urls)),
    path("", include("djoser.urls.authtoken")),
    #    path("merch/", MerchViewSet.as_view({"get": "list"})),
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
