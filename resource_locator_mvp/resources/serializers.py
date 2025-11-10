from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers
from .models import Resource


class ResourceGeoJSONSerializer(GeoFeatureModelSerializer):
    """
    Serializer that outputs GeoJSON format for map display.
    Used for anonymous/public API endpoints.
    """
    
    is_open_now = serializers.SerializerMethodField()
    
    class Meta:
        model = Resource
        geo_field = "geom"
        fields = [
            'id',
            'name',
            'rtype',
            'description',
            'hours_json',
            'phone',
            'email',
            'website',
            'address',
            'tags',
            'is_open_now',
            'created_at',
            'updated_at',
        ]
    
    def get_is_open_now(self, obj):
        """Get the current open/closed status."""
        return obj.is_open_now()


class ResourceSerializer(serializers.ModelSerializer):
    """
    Standard serializer for Resource model.
    Used for provider CRUD operations.
    """
    
    is_open_now = serializers.SerializerMethodField(read_only=True)
    provider_name = serializers.CharField(source='provider.username', read_only=True)
    
    class Meta:
        model = Resource
        fields = [
            'id',
            'name',
            'rtype',
            'description',
            'hours_json',
            'phone',
            'email',
            'website',
            'address',
            'geom',
            'tags',
            'state',
            'rejection_reason',
            'provider',
            'provider_name',
            'is_open_now',
            'expires_at',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'provider', 'created_at', 'updated_at']
    
    def get_is_open_now(self, obj):
        """Get the current open/closed status."""
        return obj.is_open_now()


class ResourceSubmissionSerializer(serializers.ModelSerializer):
    """
    Serializer for provider resource submissions.
    Limits fields that providers can set.
    """
    
    class Meta:
        model = Resource
        fields = [
            'id',
            'name',
            'rtype',
            'description',
            'hours_json',
            'phone',
            'email',
            'website',
            'address',
            'geom',
            'tags',
            'expires_at',
        ]
        read_only_fields = ['id']
    
    def validate_geom(self, value):
        """Ensure geometry is provided."""
        if not value:
            raise serializers.ValidationError("Location is required.")
        return value
