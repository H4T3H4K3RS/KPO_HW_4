from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Tasks API",
        default_version='v1',
        description="Demo Description",
        contact=openapi.Contact(email="sevavov.2004@gmail.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny, ],
)
router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
