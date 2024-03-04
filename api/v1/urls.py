from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework import routers

from api.v1.views.ambassadors_view import AmbassadorsViewSet
from api.v1.views.content_view import ContentViewSet
from api.v1.views.dropdowns_view import DropdownsViewSet
from api.v1.views.merch_view import MerchBudgetViewSet
from api.v1.views.notifications_view import NotificationViewSet
from api.v1.views.send_view import SendViewSet
from api.v1.views.promos_view import PromosViewSet
from api.v1.views.users_view import UserViewSet

v1_router = routers.DefaultRouter()
v1_router.register("ambassadors", AmbassadorsViewSet, basename="ambassadors")
v1_router.register("dropdowns", DropdownsViewSet, basename="dropdowns")
v1_router.register("content", ContentViewSet, basename="content")
v1_router.register("users", UserViewSet, basename="users")
v1_router.register("promos", PromosViewSet, basename="promos")
v1_router.register("merch", MerchBudgetViewSet, basename="merch")
v1_router.register(
    "notifications", NotificationViewSet, basename="notifications"
)

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
    path("sending/", SendViewSet.as_view(), name="product-bulk-create-update"),
]
