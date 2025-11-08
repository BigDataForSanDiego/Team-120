"""
Django forms for Waypoint model.
"""
from django import forms
from django.contrib.gis.geos import Point
from .models import Waypoint


class WaypointForm(forms.ModelForm):
    """
    Form for creating waypoints with latitude/longitude inputs.
    """
    latitude = forms.FloatField(
        min_value=-90,
        max_value=90,
        widget=forms.HiddenInput(attrs={'id': 'id_latitude'}),
        help_text="Latitude coordinate"
    )
    longitude = forms.FloatField(
        min_value=-180,
        max_value=180,
        widget=forms.HiddenInput(attrs={'id': 'id_longitude'}),
        help_text="Longitude coordinate"
    )
    
    class Meta:
        model = Waypoint
        fields = ['name', 'category', 'description', 'latitude', 'longitude']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter waypoint name'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 3,
                'placeholder': 'Optional description...'
            }),
        }
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        latitude = self.cleaned_data['latitude']
        longitude = self.cleaned_data['longitude']
        instance.location = Point(longitude, latitude, srid=4326)
        if commit:
            instance.save()
        return instance
