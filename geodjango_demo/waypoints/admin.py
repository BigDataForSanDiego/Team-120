"""
Django admin configuration for Waypoint model.
Includes geospatial widgets for map-based editing.
"""
from django.contrib.gis import admin
from .models import Waypoint


@admin.register(Waypoint)
class WaypointAdmin(admin.GISModelAdmin):
    """
    Admin interface for Waypoint model with map widget.
    """
    list_display = ['name', 'category', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'description']
    date_hierarchy = 'created_at'
    
    # GIS-specific settings
    gis_widget_kwargs = {
        'attrs': {
            'default_zoom': 10,
            'default_lon': -117.1611,  # San Diego longitude
            'default_lat': 32.7157,    # San Diego latitude
        },
    }
