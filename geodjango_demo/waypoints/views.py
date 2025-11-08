"""
Views for Waypoint model - both DRF API and Django template views.
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Waypoint
from .serializers import WaypointSerializer, WaypointCreateSerializer
from .forms import WaypointForm


class WaypointViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API ViewSet for Waypoint model.
    Provides list, retrieve, and custom filtering actions.
    """
    queryset = Waypoint.objects.all()
    serializer_class = WaypointSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['created_at', 'name']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """
        Filter queryset by category if provided.
        """
        queryset = super().get_queryset()
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        return queryset
    
    @action(detail=False, methods=['get'])
    def nearby(self, request):
        """
        Find waypoints within a specified distance from a point.
        Query params: lat, lon, distance (in kilometers, default 5)
        """
        lat = request.query_params.get('lat')
        lon = request.query_params.get('lon')
        distance_km = float(request.query_params.get('distance', 5))
        
        if not lat or not lon:
            return Response({'error': 'lat and lon parameters are required'}, status=400)
        
        point = Point(float(lon), float(lat), srid=4326)
        nearby_waypoints = Waypoint.objects.filter(
            location__distance_lte=(point, D(km=distance_km))
        ).distance(point).order_by('distance')
        
        serializer = self.get_serializer(nearby_waypoints, many=True)
        return Response(serializer.data)


def waypoint_list(request):
    """
    Display list of all waypoints.
    """
    waypoints = Waypoint.objects.all()[:20]
    categories = Waypoint.CATEGORY_CHOICES
    return render(request, 'waypoints/waypoint_list.html', {
        'waypoints': waypoints,
        'categories': categories,
    })


def waypoint_create(request):
    """
    Form view for creating a new waypoint with map picker.
    """
    if request.method == 'POST':
        form = WaypointForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Waypoint "{form.instance.name}" created successfully!')
            return redirect('waypoint_list')
    else:
        form = WaypointForm()
    
    return render(request, 'waypoints/waypoint_create.html', {'form': form})


def waypoint_map(request):
    """
    Interactive map view showing all waypoints.
    """
    return render(request, 'waypoints/waypoint_map.html')
