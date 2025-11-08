"""
Waypoint model for storing geospatial points with categories.
"""
from django.contrib.gis.db import models
from django.utils import timezone


class Waypoint(models.Model):
    """
    Represents a geographical waypoint with location and metadata.
    Uses GeoDjango's PointField with geography=True for accurate distance calculations.
    """
    CATEGORY_CHOICES = [
        ('restaurant', 'Restaurant'),
        ('park', 'Park'),
        ('museum', 'Museum'),
        ('landmark', 'Landmark'),
        ('hotel', 'Hotel'),
        ('transit', 'Transit Station'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=255, help_text="Name of the waypoint")
    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES,
        default='other',
        help_text="Category of the waypoint"
    )
    description = models.TextField(blank=True, help_text="Additional details about this waypoint")
    location = models.PointField(geography=True, help_text="Geographic coordinates (longitude, latitude)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"
