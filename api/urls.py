from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import SimpleRouter

schema_view = get_schema_view(
    openapi.Info(
        title="GSET Backend API",
        default_version="v1",
        description="API documentation for the GSET",
        terms_of_service="https://www.gset.com/terms",
        contact=openapi.Contact(email="support@gset.care"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

router = SimpleRouter(trailing_slash=False)

urlpatterns = [
    path("client/", include("api.client_api.urls")),
    # path("staff/", include("api.admin_api.urls")),
    # path("vendor/", include("api.vendor_api.urls")),
    # path("common/", include("api.common.urls")),
    path(
        "swagger<format>",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc")
]
