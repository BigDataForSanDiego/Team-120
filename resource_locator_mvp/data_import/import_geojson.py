"""
GeoJSON to Resource importer with validation and preview capabilities.

This script imports GeoJSON files into the Resource database with a two-stage process:
1. Preview: Analyze and validate the data without saving
2. Import: Save validated resources to the database
"""

import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

# Add the Django project to the Python path
# Script is in: resource_locator_mvp/data_import/import_geojson.py
# Django root is: resource_locator_mvp/
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from django.contrib.gis.geos import Point, GEOSException
from resources.models import Resource


class GeoJSONImporter:
    """Handles GeoJSON import with validation and preview."""
    
    # Mapping of common field names to Resource model fields
    FIELD_MAPPINGS = {
        'name': ['name', 'NAME', 'facility_name', 'FACILITY_NAME', 'site_name', 'SITE_NAME', 'Organization'],
        'address': ['address', 'ADDRESS', 'street_address', 'STREET_ADDRESS', 'location', 'DBA_ADDRESS1', 'ADDR', 'Address'],
        'city': ['city', 'CITY', 'DBA_CITY'],
        'zip_code': ['zip_code', 'ZIP_CODE', 'zipcode', 'ZIPCODE', 'DBA_ZIP_CODE', 'postal_code'],
        'phone': ['phone', 'PHONE', 'telephone', 'TELEPHONE', 'contact_phone', 'CONTACT_PHONE'],
        'website': ['website', 'WEBSITE', 'url', 'URL', 'web_address', 'WEB_ADDRESS'],
        'description': ['description', 'DESCRIPTION', 'notes', 'NOTES', 'comments', 'COMMENTS'],
        'hours': ['hours', 'HOURS', 'hours_of_operation', 'HOURS_OF_OPERATION', 'operating_hours', 'OPERATING_HOURS', 'OperationalHours'],
    }
    
    # Resource type keywords for automatic classification
    TYPE_KEYWORDS = {
        'medical': ['hospital', 'clinic', 'health', 'medical', 'doctor', 'physician', 
                    'healthcare', 'care center', 'emergency', 'urgent care', 'surgery'],
        'food': ['food', 'meal', 'pantry', 'kitchen', 'soup', 'nutrition'],
        'shelter': ['shelter', 'housing', 'homeless', 'transitional', 'cool zone', 'cooling center', 'cooling station'],
        'legal': ['legal', 'law', 'attorney', 'court'],
        'restroom': ['restroom', 'bathroom', 'toilet', 'washroom'],
        'donation': ['donation', 'thrift', 'goodwill', 'charity'],
    }
    
    def __init__(self, geojson_path: str, resource_type: Optional[str] = None):
        """
        Initialize the importer.
        
        Args:
            geojson_path: Path to the GeoJSON file
            resource_type: Optional resource type to assign to all features
        """
        self.geojson_path = Path(geojson_path)
        self.default_resource_type = resource_type
        self.features = []
        self.parsed_resources = []
        self.validation_errors = []
        
    def load_geojson(self) -> bool:
        """Load and parse the GeoJSON file."""
        try:
            with open(self.geojson_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if data.get('type') != 'FeatureCollection':
                print(f"❌ Error: Not a valid FeatureCollection")
                return False
            
            self.features = data.get('features', [])
            print(f"✅ Loaded {len(self.features)} features from {self.geojson_path.name}")
            return True
            
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing JSON: {e}")
            return False
        except FileNotFoundError:
            print(f"❌ Error: File not found: {self.geojson_path}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
    
    def _find_field_value(self, properties: Dict, field_type: str) -> Optional[str]:
        """Find a field value from properties using field mappings."""
        possible_fields = self.FIELD_MAPPINGS.get(field_type, [])
        
        for field_name in possible_fields:
            if field_name in properties:
                value = properties[field_name]
                if value and str(value).strip():
                    return str(value).strip()
        
        return None
    
    def _construct_address(self, properties: Dict) -> str:
        """Construct a full address from separate address fields."""
        # Try to find a complete address first
        full_address = self._find_field_value(properties, 'address')
        if full_address:
            return full_address
        
        # Otherwise, construct from parts
        address_parts = []
        
        street = self._find_field_value(properties, 'address')
        if street:
            address_parts.append(street)
        
        city = self._find_field_value(properties, 'city')
        if city:
            address_parts.append(city)
        
        zip_code = self._find_field_value(properties, 'zip_code')
        if zip_code:
            address_parts.append(str(zip_code))
        
        return ', '.join(address_parts) if address_parts else ''
    
    def _extract_hours(self, properties: Dict) -> Dict:
        """
        Extract and parse hours of operation into the expected JSON format.
        
        Expected format: {"mon":[[\"09:00\",\"17:00\"]], "tue":[[\"09:00\",\"17:00\"]], ...}
        
        Returns:
            Dict with hours, or empty dict if no hours found
        """
        # Try to find hours field
        hours_str = self._find_field_value(properties, 'hours')
        
        if not hours_str:
            # Check for individual day fields
            days_map = {
                'mon': ['monday', 'mon', 'MONDAY', 'MON'],
                'tue': ['tuesday', 'tue', 'TUESDAY', 'TUE'],
                'wed': ['wednesday', 'wed', 'WEDNESDAY', 'WED'],
                'thu': ['thursday', 'thu', 'THURSDAY', 'THU'],
                'fri': ['friday', 'fri', 'FRIDAY', 'FRI'],
                'sat': ['saturday', 'sat', 'SATURDAY', 'SAT'],
                'sun': ['sunday', 'sun', 'SUNDAY', 'SUN'],
            }
            
            hours_json = {}
            for day_key, possible_names in days_map.items():
                for field_name in possible_names:
                    if field_name in properties and properties[field_name]:
                        # Try to parse the hours
                        hours_json[day_key] = self._parse_day_hours(properties[field_name])
                        break
            
            return hours_json if hours_json else {}
        
        # Try to parse structured hours string
        # Common formats:
        # - "Mon-Fri: 9:00 AM - 5:00 PM"
        # - "24/7"
        # - "Always Open"
        # - JSON string
        
        hours_str_lower = hours_str.lower().strip()
        
        # Check for 24/7 or always open
        if '24/7' in hours_str_lower or 'always open' in hours_str_lower or '24 hours' in hours_str_lower:
            return {
                'mon': [['00:00', '23:59']],
                'tue': [['00:00', '23:59']],
                'wed': [['00:00', '23:59']],
                'thu': [['00:00', '23:59']],
                'fri': [['00:00', '23:59']],
                'sat': [['00:00', '23:59']],
                'sun': [['00:00', '23:59']],
            }
        
        # Try to parse as JSON first
        try:
            parsed = json.loads(hours_str)
            if isinstance(parsed, dict):
                return parsed
        except (json.JSONDecodeError, ValueError):
            pass
        
        # Try to parse multi-line format (e.g., "Mon 12:00pm-8:00pm\nTues 12:00pm-8:00pm...")
        if '\n' in hours_str or any(day in hours_str for day in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']):
            return self._parse_multiline_hours(hours_str)
        
        # For other formats, store as description in tags or return empty
        # This can be enhanced later with more sophisticated parsing
        return {}
    
    def _parse_multiline_hours(self, hours_str: str) -> Dict:
        """
        Parse multi-line hours format into hours_json structure.
        
        Example input:
            "Mon 12:00pm-8:00pm\\nTues 12:00pm-8:00pm\\nWed 12:00pm-8:00pm..."
            
        Returns:
            Dict in format {"mon": [["12:00", "20:00"]], "tue": [...], ...}
        """
        import re
        
        # Day name mapping
        day_mapping = {
            'mon': ['mon', 'monday'],
            'tue': ['tue', 'tues', 'tuesday'],
            'wed': ['wed', 'wednesday'],
            'thu': ['thu', 'thur', 'thurs', 'thursday'],
            'fri': ['fri', 'friday'],
            'sat': ['sat', 'saturday'],
            'sun': ['sun', 'sunday'],
        }
        
        hours_json = {}
        
        # Split by newlines and process each line
        lines = hours_str.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Skip lines that are obviously not day schedules (like "Observed Holidays")
            if 'holiday' in line.lower() or 'observe' in line.lower():
                continue
            
            # Try to match pattern: "Day HH:MMam/pm-HH:MMam/pm" or "Day Closed"
            # Pattern to find day name at start of line
            found_day = None
            day_key = None
            
            for key, variations in day_mapping.items():
                for variation in variations:
                    if line.lower().startswith(variation):
                        found_day = variation
                        day_key = key
                        break
                if found_day:
                    break
            
            if not day_key:
                continue
            
            # Remove the day name from the line to get just the hours part
            hours_part = line[len(found_day):].strip()
            
            # Check if closed
            if 'closed' in hours_part.lower():
                hours_json[day_key] = []
                continue
            
            # Parse time range (e.g., "12:00pm-8:00pm" or "12:00 pm - 8:00 pm")
            # Pattern: HH:MM[am|pm] - HH:MM[am|pm]
            time_pattern = r'(\d{1,2}):(\d{2})\s*(am|pm)\s*[-–]\s*(\d{1,2}):(\d{2})\s*(am|pm)'
            match = re.search(time_pattern, hours_part, re.IGNORECASE)
            
            if match:
                start_hour = int(match.group(1))
                start_min = match.group(2)
                start_period = match.group(3).lower()
                end_hour = int(match.group(4))
                end_min = match.group(5)
                end_period = match.group(6).lower()
                
                # Convert to 24-hour format
                if start_period == 'pm' and start_hour != 12:
                    start_hour += 12
                elif start_period == 'am' and start_hour == 12:
                    start_hour = 0
                
                if end_period == 'pm' and end_hour != 12:
                    end_hour += 12
                elif end_period == 'am' and end_hour == 12:
                    end_hour = 0
                
                hours_json[day_key] = [[f"{start_hour:02d}:{start_min}", f"{end_hour:02d}:{end_min}"]]
        
        return hours_json
    
    def _parse_day_hours(self, hours_str: str) -> List:
        """
        Parse a single day's hours string into [[start, end]] format.
        
        Examples:
            "9:00 AM - 5:00 PM" -> [["09:00", "17:00"]]
            "9-5" -> [["09:00", "17:00"]]
            "Closed" -> []
        """
        if not hours_str or isinstance(hours_str, (int, float)):
            return []
        
        hours_str = str(hours_str).strip().lower()
        
        if 'closed' in hours_str or 'n/a' in hours_str:
            return []
        
        if '24' in hours_str and 'hour' in hours_str:
            return [['00:00', '23:59']]
        
        # Try to extract time ranges
        # This is a simple implementation - can be enhanced
        import re
        
        # Look for patterns like "9:00 AM - 5:00 PM" or "09:00-17:00"
        time_pattern = r'(\d{1,2}):?(\d{2})?\s*(am|pm)?\s*[-–]\s*(\d{1,2}):?(\d{2})?\s*(am|pm)?'
        match = re.search(time_pattern, hours_str, re.IGNORECASE)
        
        if match:
            start_hour = int(match.group(1))
            start_min = match.group(2) or '00'
            start_period = match.group(3)
            end_hour = int(match.group(4))
            end_min = match.group(5) or '00'
            end_period = match.group(6)
            
            # Convert to 24-hour format
            if start_period and start_period.lower() == 'pm' and start_hour != 12:
                start_hour += 12
            elif start_period and start_period.lower() == 'am' and start_hour == 12:
                start_hour = 0
                
            if end_period and end_period.lower() == 'pm' and end_hour != 12:
                end_hour += 12
            elif end_period and end_period.lower() == 'am' and end_hour == 12:
                end_hour = 0
            
            return [[f"{start_hour:02d}:{start_min}", f"{end_hour:02d}:{end_min}"]]
        
        return []
    
    def _infer_resource_type(self, properties: Dict) -> str:
        """Infer resource type from properties."""
        if self.default_resource_type:
            return self.default_resource_type
        
        # Check if this is a Cool Zone based on filename
        if 'cool_zone' in str(self.geojson_path).lower() or 'cool zone' in str(self.geojson_path).lower():
            return 'shelter'
        
        # Check all text fields for keywords
        text_fields = []
        for key, value in properties.items():
            if isinstance(value, str):
                text_fields.append(value)
        
        text_to_check = ' '.join(text_fields).lower()
        
        for rtype, keywords in self.TYPE_KEYWORDS.items():
            if any(keyword in text_to_check for keyword in keywords):
                return rtype
        
        return 'other'
    
    def _extract_geometry(self, geometry: Dict) -> Optional[Point]:
        """Extract Point geometry from GeoJSON geometry object."""
        try:
            if geometry['type'] == 'Point':
                coords = geometry['coordinates']
                # GeoJSON is [lon, lat], Django expects Point(lon, lat)
                return Point(coords[0], coords[1], srid=4326)
            else:
                print(f"⚠️  Warning: Unsupported geometry type: {geometry['type']}")
                return None
        except (KeyError, IndexError, GEOSException) as e:
            print(f"⚠️  Warning: Invalid geometry: {e}")
            return None
    
    def parse_features(self) -> List[Dict]:
        """Parse features into Resource-compatible dictionaries."""
        self.parsed_resources = []
        self.validation_errors = []
        
        for idx, feature in enumerate(self.features):
            try:
                properties = feature.get('properties', {})
                geometry = feature.get('geometry', {})
                
                # Extract required fields
                name = self._find_field_value(properties, 'name')
                geom = self._extract_geometry(geometry)
                
                # Skip if missing required fields
                if not name:
                    self.validation_errors.append({
                        'index': idx,
                        'error': 'Missing required field: name',
                        'properties': properties
                    })
                    continue
                
                if not geom:
                    self.validation_errors.append({
                        'index': idx,
                        'error': 'Invalid or missing geometry',
                        'name': name
                    })
                    continue
                
                # Build resource dict
                resource_data = {
                    'name': name,
                    'rtype': self._infer_resource_type(properties),
                    'geom': geom,
                    'address': self._construct_address(properties),
                    'phone': self._find_field_value(properties, 'phone') or '',
                    'website': self._find_field_value(properties, 'website') or '',
                    'description': self._find_field_value(properties, 'description') or '',
                    'state': 'visible',  # All new data will be visible during development
                    # 'state': 'not_visible',  # New imports start as not_visible for review
                    'tags': [],
                    'hours_json': self._extract_hours(properties),
                    'raw_properties': properties,  # Store for reference
                }
                
                self.parsed_resources.append(resource_data)
                
            except Exception as e:
                self.validation_errors.append({
                    'index': idx,
                    'error': f'Parsing error: {str(e)}',
                    'feature': feature
                })
        
        return self.parsed_resources
    
    def preview(self, limit: int = 10) -> None:
        """Display a preview of parsed resources."""
        print("\n" + "="*80)
        print("IMPORT PREVIEW")
        print("="*80)
        
        print(f"\n📊 Statistics:")
        print(f"  • Total features: {len(self.features)}")
        print(f"  • Successfully parsed: {len(self.parsed_resources)}")
        print(f"  • Validation errors: {len(self.validation_errors)}")
        
        # Count resources with hours
        resources_with_hours = sum(1 for r in self.parsed_resources if r.get('hours_json'))
        print(f"  • Resources with hours: {resources_with_hours}")
        print(f"  • Resources without hours: {len(self.parsed_resources) - resources_with_hours}")
        
        # Resource type distribution
        type_counts = {}
        for resource in self.parsed_resources:
            rtype = resource['rtype']
            type_counts[rtype] = type_counts.get(rtype, 0) + 1
        
        print(f"\n📦 Resource Types:")
        for rtype, count in sorted(type_counts.items()):
            print(f"  • {rtype}: {count}")
        
        # Show sample resources
        print(f"\n📋 Sample Resources (showing up to {limit}):")
        print("-" * 80)
        
        for i, resource in enumerate(self.parsed_resources[:limit]):
            print(f"\n[{i+1}] {resource['name']}")
            print(f"    Type: {resource['rtype']}")
            print(f"    Location: ({resource['geom'].y:.6f}, {resource['geom'].x:.6f})")
            if resource['address']:
                print(f"    Address: {resource['address']}")
            if resource['phone']:
                print(f"    Phone: {resource['phone']}")
            if resource['website']:
                print(f"    Website: {resource['website'][:60]}...")
            if resource.get('hours_json'):
                print(f"    Hours: {len(resource['hours_json'])} days configured")
            else:
                print(f"    Hours: Not available")
        
        # Show validation errors
        if self.validation_errors:
            print(f"\n⚠️  Validation Errors (showing first 5):")
            print("-" * 80)
            for error in self.validation_errors[:5]:
                print(f"\nFeature #{error.get('index', 'unknown')}:")
                print(f"  Error: {error['error']}")
                if 'name' in error:
                    print(f"  Name: {error['name']}")
        
        print("\n" + "="*80)
    
    def save_preview_to_file(self, output_path: str) -> None:
        """Save detailed preview to a JSON file for review."""
        resources_with_hours = sum(1 for r in self.parsed_resources if r.get('hours_json'))
        
        preview_data = {
            'import_date': datetime.now().isoformat(),
            'source_file': str(self.geojson_path),
            'statistics': {
                'total_features': len(self.features),
                'parsed': len(self.parsed_resources),
                'errors': len(self.validation_errors),
                'resources_with_hours': resources_with_hours,
                'resources_without_hours': len(self.parsed_resources) - resources_with_hours,
            },
            'resources': [
                {
                    'name': r['name'],
                    'rtype': r['rtype'],
                    'address': r['address'],
                    'phone': r['phone'],
                    'website': r['website'],
                    'description': r['description'],
                    'hours_json': r['hours_json'],
                    'latitude': r['geom'].y,
                    'longitude': r['geom'].x,
                    'raw_properties': r['raw_properties'],
                }
                for r in self.parsed_resources
            ],
            'validation_errors': self.validation_errors,
        }
        
        output_file = Path(output_path)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(preview_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Preview saved to: {output_file}")
    
    def import_to_database(self, dry_run: bool = False) -> Tuple[int, int]:
        """
        Import parsed resources to database.
        
        Args:
            dry_run: If True, don't actually save to database
            
        Returns:
            Tuple of (created_count, skipped_count)
        """
        if not self.parsed_resources:
            print("❌ No resources to import. Run parse_features() first.")
            return 0, 0
        
        created_count = 0
        skipped_count = 0
        
        print("\n" + "="*80)
        print("IMPORTING TO DATABASE")
        print("="*80)
        
        if dry_run:
            print("\n🔍 DRY RUN MODE - No changes will be saved\n")
        
        for i, resource_data in enumerate(self.parsed_resources):
            try:
                # Remove raw_properties before saving
                raw_props = resource_data.pop('raw_properties', None)
                
                # Check if resource already exists
                existing = Resource.objects.filter(
                    name=resource_data['name'],
                    geom__distance_lte=(resource_data['geom'], 100)  # Within 100 meters
                ).first()
                
                if existing:
                    print(f"⏭️  Skipped: {resource_data['name']} (already exists)")
                    skipped_count += 1
                    continue
                
                if not dry_run:
                    resource = Resource.objects.create(**resource_data)
                    print(f"✅ Created: {resource.name}")
                else:
                    print(f"✓  Would create: {resource_data['name']}")
                
                created_count += 1
                
            except Exception as e:
                print(f"❌ Error creating resource: {resource_data.get('name', 'unknown')}")
                print(f"   Error: {str(e)}")
                skipped_count += 1
        
        print("\n" + "="*80)
        print(f"Summary:")
        print(f"  • Created: {created_count}")
        print(f"  • Skipped: {skipped_count}")
        print("="*80)
        
        return created_count, skipped_count


def main():
    """Main CLI interface."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Import GeoJSON data into Resource database',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Preview the import
  python import_geojson.py data.geojson --preview
  
  # Save preview to file
  python import_geojson.py data.geojson --preview --output preview.json
  
  # Dry run (don't save to database)
  python import_geojson.py data.geojson --import --dry-run
  
  # Actually import
  python import_geojson.py data.geojson --import
  
  # Specify resource type
  python import_geojson.py data.geojson --type medical --import
        """
    )
    
    parser.add_argument('geojson_file', help='Path to GeoJSON file')
    parser.add_argument('--type', choices=['food', 'shelter', 'restroom', 'medical', 'legal', 'donation', 'other'],
                        help='Force all resources to this type (otherwise auto-detected)')
    parser.add_argument('--preview', action='store_true', help='Show preview of data')
    parser.add_argument('--output', help='Save preview to JSON file')
    parser.add_argument('--import', dest='do_import', action='store_true', help='Import to database')
    parser.add_argument('--dry-run', action='store_true', help='Dry run (don\'t save to database)')
    parser.add_argument('--limit', type=int, default=10, help='Number of samples to show in preview')
    
    args = parser.parse_args()
    
    # Initialize importer
    importer = GeoJSONImporter(args.geojson_file, resource_type=args.type)
    
    # Load GeoJSON
    if not importer.load_geojson():
        sys.exit(1)
    
    # Parse features
    importer.parse_features()
    
    # Show preview
    if args.preview or not args.do_import:
        importer.preview(limit=args.limit)
        
        if args.output:
            importer.save_preview_to_file(args.output)
    
    # Import to database
    if args.do_import:
        response = input("\n⚠️  Proceed with import? [y/N]: ")
        if response.lower() == 'y':
            importer.import_to_database(dry_run=args.dry_run)
        else:
            print("Import cancelled.")
    
    print("\n✅ Done!")


if __name__ == '__main__':
    main()