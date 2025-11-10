from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResourceViewSet, ProviderResourceViewSet, AdminResourceViewSet
from . import provider_views

# Create routers for API endpoints
router = DefaultRouter()
router.register(r'resources', ResourceViewSet, basename='resource')
router.register(r'provider/resources', ProviderResourceViewSet, basename='provider-resource')
router.register(r'admin/resources', AdminResourceViewSet, basename='admin-resource')

app_name = 'resources'

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
    
    # Provider dashboard and CRUD views
    path('provider/', provider_views.provider_dashboard, name='provider_dashboard'),
    path('provider/resource/create/', provider_views.provider_resource_create, name='provider_resource_create'),
    path('provider/resource/<int:pk>/edit/', provider_views.provider_resource_edit, name='provider_resource_edit'),
    path('provider/resource/<int:pk>/delete/', provider_views.provider_resource_delete, name='provider_resource_delete'),
]
