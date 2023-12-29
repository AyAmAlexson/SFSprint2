
from django.contrib import admin
from django.urls import path, include, re_path

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Mountain Pass API for SF internship",
        default_version='v1',
        description="REST API for managing mountain passes. \
            Tourists can submit information about a mountain pass, including coordinates, \
            height, name, images, and user details, through the `submitData` endpoint. \
            The submitted data is stored in a database, and users can retrieve, edit, \
            or list their submitted mountain passes.",
        contact=openapi.Contact(email="a.molodenko@gmail.com"),
    ),
    public=True,
    permission_classes=(
        permissions.AllowAny,
    ),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('mountapi.urls')),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
