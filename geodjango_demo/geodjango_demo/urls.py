"""
URL Configuration for geodjango_demo project.
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from waypoints.views import WaypointViewSet, waypoint_list, waypoint_create, waypoint_map

# REST API Router
router = DefaultRouter()
router.register(r'waypoints', WaypointViewSet, basename='waypoint')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('', waypoint_list, name='waypoint_list'),
    path('create/', waypoint_create, name='waypoint_create'),
    path('map/', waypoint_map, name='waypoint_map'),
]
