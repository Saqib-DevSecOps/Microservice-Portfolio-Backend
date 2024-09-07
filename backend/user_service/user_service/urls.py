
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Personal Portfolio Site",
        default_version="1.0",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# EXTERNAL APPS URLS
urlpatterns = [

    # DJANGO URLS > remove in extreme security
    path('admin/', admin.site.urls),

    # SWAGGER
    re_path(r'^api(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^api$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    # REST-AUTH URLS
    re_path('rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    re_path('rest-auth/', include('dj_rest_auth.urls')),
]


# your apps urls
urlpatterns += [
    # path('', include('src.website.urls', namespace='website')),

]

