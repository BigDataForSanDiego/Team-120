"""
DRF Serializers for Waypoint model.
Uses GeoFeatureModelSerializer for GeoJSON output.
"""
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers
from .models import Waypoint


class WaypointSerializer(GeoFeatureModelSerializer):
    """
    GeoJSON serializer for Waypoint model.
    Outputs valid GeoJSON FeatureCollection format for map rendering.
    """
    class Meta:
        model = Waypoint
        geo_field = "location"
        fields = ('id', 'name', 'category', 'description', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')


class WaypointCreateSerializer(serializers.ModelSerializer):
    """
    Standard serializer for creating waypoints via forms.
    """
    longitude = serializers.FloatField(write_only=True)
    latitude = serializers.FloatField(write_only=True)
    
    class Meta:
        model = Waypoint
        fields = ('name', 'category', 'description', 'longitude', 'latitude')
    
    def create(self, validated_data):
        from django.contrib.gis.geos import Point
        longitude = validated_data.pop('longitude')
        latitude = validated_data.pop('latitude')
        validated_data['location'] = Point(longitude, latitude, srid=4326)
        return super().create(validated_data)
