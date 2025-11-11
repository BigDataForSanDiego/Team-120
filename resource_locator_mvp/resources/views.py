from rest_framework import viewsets, filters, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from .models import Resource
from .serializers import (
    ResourceGeoJSONSerializer,
    ResourceSerializer,
    
    ResourceSubmissionSerializer
)
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import viewsets
from .models import Resource
from .serializers import ResourceSerializer


from django.db.models import Q

class ResourceViewSet(viewsets.ReadOnlyModelViewSet):

    """
    Public read-only API for resources.
    Returns GeoJSON format suitable for map rendering.
    
    Query parameters:
    - rtype: Filter by resource type (comma-separated, e.g., "food,shelter")
    - lat, lon: User location for distance filtering
    - radius_m: Radius in meters (default 5000m = ~3 miles)
    - open_now: Filter to only open resources (true/false)
    """
    
    serializer_class = ResourceGeoJSONSerializer
    permission_classes = [permissions.AllowAny]
    # Return GeoJSON FeatureCollection directly for the map frontend (no DRF pagination)
    pagination_class = None
    
    def get_queryset(self):
        queryset = Resource.objects.filter(state__in=['visible', 'approved'])

        # Filter by resource type (case-insensitive)
        rtype_param = self.request.query_params.get('rtype', None)
        if rtype_param:
            types = [t.strip() for t in rtype_param.split(',')]
            q_obj = Q()
            for t in types:
                q_obj |= Q(rtype__iexact=t)
            queryset = queryset.filter(q_obj)

        # Filter by location and radius
        lat = self.request.query_params.get('lat', None)
        lon = self.request.query_params.get('lon', None)
        radius_m = self.request.query_params.get('radius_m', 5000)

        if lat and lon:
            try:
                user_location = Point(float(lon), float(lat), srid=4326)
                radius_m = float(radius_m)
                queryset = (
                    queryset.filter(geom__dwithin=(user_location, D(m=radius_m)))
                    .annotate(distance=Distance('geom', user_location))
                    .order_by('distance')
                )
            except (ValueError, TypeError):
                pass

        # Optional "open now" filter
        open_now = self.request.query_params.get('open_now', '').lower()
        if open_now == 'true':
            resource_ids = [r.id for r in queryset if r.is_open_now()]
            queryset = queryset.filter(id__in=resource_ids)

        print(f"[DEBUG] Filters: rtype={rtype_param}, count={queryset.count()}")
        return queryset


class ProviderResourceViewSet(viewsets.ModelViewSet):
    """
    Provider API for managing their own resources.
    Requires authentication.
    """
    
    serializer_class = ResourceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return only resources owned by the current user."""
        return Resource.objects.filter(provider=self.request.user)
    
    def get_serializer_class(self):
        """Use submission serializer for create/update."""
        if self.action in ['create', 'update', 'partial_update']:
            return ResourceSubmissionSerializer
        return ResourceSerializer
    
    def perform_create(self, serializer):
        """Set provider to current user and state to visible on creation."""
        serializer.save(
            provider=self.request.user,
            state='visible'
        )
    
    def perform_update(self, serializer):
        """Only allow updates if resource is visible or not_visible."""
        instance = self.get_object()
        if instance.state not in ['visible', 'not_visible']:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied(
                "Cannot edit resources in 'rejected' state."
            )
        serializer.save()


class AdminResourceViewSet(viewsets.ModelViewSet):
    """
    Admin API for managing all resources.
    Full CRUD access with moderation capabilities.
    """
    
    serializer_class = ResourceSerializer
    permission_classes = [permissions.IsAdminUser]
    
    def get_queryset(self):
        """Return all resources, with optional state filter."""
        queryset = Resource.objects.all().select_related('provider')
        
        # Filter by state
        state_param = self.request.query_params.get('state', None)
        if state_param:
            queryset = queryset.filter(state=state_param)
        
        return queryset.order_by('-created_at')
    
    @action(detail=True, methods=['patch'])
    def moderate(self, request, pk=None):
        """
        Moderate a resource: approve, hide, or reject.
        
        Body:
        {
            "state": "visible" | "not_visible" | "rejected",
            "rejection_reason": "optional reason for rejection"
        }
        """
        resource = self.get_object()
        new_state = request.data.get('state')
        
        if new_state not in ['visible', 'not_visible', 'rejected']:
            return Response(
                {'error': 'Invalid state. Must be visible, not_visible, or rejected.'},
                status=400
            )
        
        resource.state = new_state
        
        if new_state == 'rejected':
            resource.rejection_reason = request.data.get('rejection_reason', '')
        
        resource.save()
        
        serializer = self.get_serializer(resource)
        return Response(serializer.data)

