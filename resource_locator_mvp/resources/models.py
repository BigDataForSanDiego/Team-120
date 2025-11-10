from django.contrib.gis.db import models
from django.conf import settings
from django.utils import timezone


class Resource(models.Model):
    """
    Resource model representing a location providing services 
    (food, shelter, medical, etc.) for people experiencing homelessness.
    """
    
    TYPE_CHOICES = [
        ("food", "Food"),
        ("shelter", "Shelter"),
        ("restroom", "Restroom"),
        ("medical", "Medical"),
        ("legal", "Legal"),
        ("donation", "Donation Location"),
        ("other", "Other"),
    ]
    
    STATE_CHOICES = [
        ("visible", "Visible"),
        ("not_visible", "Not Visible"),
        ("rejected", "Rejected"),
    ]
    
    # Basic Information
    name = models.CharField(max_length=200, help_text="Name of the resource/location")
    rtype = models.CharField(
        max_length=20, 
        choices=TYPE_CHOICES,
        verbose_name="Resource Type",
        help_text="Category of service provided"
    )
    description = models.TextField(
        blank=True,
        help_text="Detailed description of services offered"
    )
    
    # Hours of Operation
    hours_json = models.JSONField(
        default=dict,
        blank=True,
        help_text='Weekly schedule in format: {"mon":[[\"09:00\",\"17:00\"]], "tue":...}'
    )
    
    # Contact Information
    phone = models.CharField(max_length=40, blank=True, help_text="Contact phone number")
    email = models.EmailField(blank=True, help_text="Contact email address")
    website = models.URLField(blank=True, help_text="Website URL")
    
    # Location
    address = models.CharField(max_length=255, blank=True, help_text="Street address")
    geom = models.PointField(
        geography=True,
        help_text="Geographic location (point)"
    )
    
    # Metadata
    tags = models.JSONField(
        default=list,
        blank=True,
        help_text="Additional tags/keywords as a list"
    )
    
    # State and Moderation
    state = models.CharField(
        max_length=15,
        choices=STATE_CHOICES,
        default="visible",
        help_text="Visibility and moderation state"
    )
    rejection_reason = models.TextField(
        blank=True,
        help_text="Reason for rejection (if state is rejected)"
    )
    
    # Ownership
    provider = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='resources',
        help_text="Service provider who submitted this resource"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Optional expiration date for time-limited resources"
    )
    
    class Meta:
        indexes = [
            models.Index(fields=["rtype", "state"]),
            models.Index(fields=["state"]),
            models.Index(fields=["provider"]),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.get_rtype_display()})"
    
    def is_open_now(self):
        """
        Check if the resource is currently open based on hours_json.
        Returns True if open, False if closed, None if no hours specified.
        """
        if not self.hours_json:
            return None
        
        now = timezone.localtime()
        weekday = now.strftime('%a').lower()  # 'mon', 'tue', etc.
        current_time = now.time()
        
        day_hours = self.hours_json.get(weekday, [])
        
        for time_range in day_hours:
            if len(time_range) != 2:
                continue
            
            try:
                from datetime import datetime
                start_time = datetime.strptime(time_range[0], '%H:%M').time()
                end_time = datetime.strptime(time_range[1], '%H:%M').time()
                
                # Handle overnight hours (e.g., 23:00 to 02:00)
                if start_time <= end_time:
                    if start_time <= current_time < end_time:
                        return True
                else:
                    if current_time >= start_time or current_time < end_time:
                        return True
            except (ValueError, IndexError):
                continue
        
        return False
    
    def is_expired(self):
        """Check if resource has expired."""
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False

