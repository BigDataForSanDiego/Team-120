from django import forms
from django.contrib.gis.geos import Point
from .models import Resource


class ResourceSubmissionForm(forms.ModelForm):
    """Form for providers to submit/edit resources."""
    
    # Separate fields for latitude and longitude
    latitude = forms.FloatField(
        required=True,
        widget=forms.HiddenInput(),
        help_text="Click on the map to set location"
    )
    longitude = forms.FloatField(
        required=True,
        widget=forms.HiddenInput(),
        help_text="Click on the map to set location"
    )
    
    class Meta:
        model = Resource
        fields = [
            'name',
            'rtype',
            'description',
            'address',
            'phone',
            'email',
            'website',
            'hours_json',
            'tags',
            'expires_at',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'hours_json': forms.Textarea(attrs={
                'rows': 6,
                'placeholder': '{"mon": [["09:00", "17:00"]], "tue": [["09:00", "17:00"]]}'
            }),
            'tags': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': '["tag1", "tag2", "tag3"]'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # If editing existing resource, populate lat/lon from geom
        if self.instance and self.instance.pk:
            self.fields['latitude'].initial = self.instance.geom.y
            self.fields['longitude'].initial = self.instance.geom.x
    
    def clean(self):
        cleaned_data = super().clean()
        lat = cleaned_data.get('latitude')
        lon = cleaned_data.get('longitude')
        
        if lat is None or lon is None:
            raise forms.ValidationError('Please select a location on the map.')
        
        # Validate latitude and longitude ranges
        if not (-90 <= lat <= 90):
            raise forms.ValidationError('Invalid latitude value.')
        
        if not (-180 <= lon <= 180):
            raise forms.ValidationError('Invalid longitude value.')
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Create Point geometry from lat/lon
        lat = self.cleaned_data['latitude']
        lon = self.cleaned_data['longitude']
        instance.geom = Point(lon, lat, srid=4326)
        
        if commit:
            instance.save()
        
        return instance
