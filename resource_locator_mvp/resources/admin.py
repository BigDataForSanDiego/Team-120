from django.contrib.gis import admin
from .models import Resource


@admin.register(Resource)
class ResourceAdmin(admin.GISModelAdmin):
    """
    Admin interface for Resource model with map widget for geometry editing.
    """
    
    # Map widget configuration
    gis_widget_kwargs = {
        'attrs': {
            'default_lat': 32.7157,  # San Diego latitude
            'default_lon': -117.1611,  # San Diego longitude
            'default_zoom': 11,
        },
    }
    
    # List display
    list_display = [
        'name',
        'rtype',
        'state',
        'provider',
        'created_at',
        'updated_at',
    ]
    
    # Filters in sidebar
    list_filter = [
        'state',
        'rtype',
        'created_at',
        'updated_at',
    ]
    
    # Search functionality
    search_fields = [
        'name',
        'description',
        'address',
        'phone',
        'email',
    ]
    
    # Field organization in detail view
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'rtype', 'description')
        }),
        ('Location', {
            'fields': ('address', 'geom')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'website'),
            'classes': ('collapse',)
        }),
        ('Hours of Operation', {
            'fields': ('hours_json',),
            'classes': ('collapse',)
        }),
        ('Moderation', {
            'fields': ('state', 'rejection_reason', 'provider')
        }),
        ('Metadata', {
            'fields': ('tags', 'expires_at', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Read-only fields
    readonly_fields = ['created_at', 'updated_at']
    
    # Ordering
    ordering = ['-created_at']
    
    # Items per page
    list_per_page = 50
    
    def get_queryset(self, request):
        """Optimize queryset with select_related for provider."""
        qs = super().get_queryset(request)
        return qs.select_related('provider')

