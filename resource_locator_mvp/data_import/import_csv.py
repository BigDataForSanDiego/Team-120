"""
CSV to Resource importer with validation and preview capabilities.

This script imports CSV files into the Resource database with a two-stage process:
1. Preview: Analyze and validate the data without saving
2. Import: Save validated resources to the database
"""

import csv
import json
import sys
import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

# Add the Django project to the Python path
# Script is in: resource_locator_mvp/data_import/import_csv.py
# Django root is: resource_locator_mvp/
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from django.contrib.gis.geos import Point, GEOSException
from resources.models import Resource


class CSVImporter:
    """Handles CSV import with validation and preview."""
    
    # Mapping of common column names to Resource model fields
    FIELD_MAPPINGS = {
        'name': ['name', 'NAME', 'Name', 'facility_name', 'FACILITY_NAME', 'organization', 'Organization'],
        'rtype': ['rtype', 'type', 'resource_type', 'category', 'Category'],
        'address': ['address', 'ADDRESS', 'Address', 'street_address', 'location', 'Location'],
        'phone': ['phone', 'PHONE', 'Phone', 'telephone', 'contact_phone', 'Contact'],
        'email': ['email', 'EMAIL', 'Email', 'contact_email'],
        'website': ['website', 'WEBSITE', 'Website', 'url', 'URL', 'web_address'],
        'description': ['description', 'DESCRIPTION', 'Description', 'notes', 'Notes', 'comments'],
        'hours_json': ['hours_json', 'hours', 'Hours', 'operating_hours', 'operational_hours'],
        'tags': ['tags', 'Tags', 'TAGS', 'keywords'],
        'latitude': ['lat', 'Lat', 'LAT', 'latitude', 'Latitude', 'LATITUDE'],
        'longitude': ['lon', 'Long', 'LONG', 'longitude', 'Longitude', 'LONGITUDE', 'lng'],
        'geom': ['geom', 'geometry', 'wkt', 'point'],
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
    
    def __init__(self, csv_path: str, resource_type: Optional[str] = None):
        """
        Initialize the importer.
        
        Args:
            csv_path: Path to the CSV file
            resource_type: Optional resource type to assign to all entries
        """
        self.csv_path = Path(csv_path)
        self.default_resource_type = resource_type
        self.rows = []
        self.headers = []
        self.parsed_resources = []
        self.validation_errors = []
        
    def load_csv(self) -> bool:
        """Load and parse the CSV file."""
        try:
            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
            loaded = False
            
            for encoding in encodings:
                try:
                    with open(self.csv_path, 'r', encoding=encoding) as f:
                        reader = csv.DictReader(f)
                        self.headers = reader.fieldnames
                        self.rows = list(reader)
                    loaded = True
                    if encoding != 'utf-8':
                        print(f"ℹ️  Note: File loaded with {encoding} encoding")
                    break
                except UnicodeDecodeError:
                    continue
            
            if not loaded:
                print(f"❌ Error: Could not decode file with any known encoding")
                return False
            
            print(f"✅ Loaded {len(self.rows)} rows from {self.csv_path.name}")
            print(f"📋 Detected columns: {', '.join(self.headers[:10])}")
            if len(self.headers) > 10:
                print(f"   ... and {len(self.headers) - 10} more")
            return True
            
        except FileNotFoundError:
            print(f"❌ Error: File not found: {self.csv_path}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            return False
    
    def _find_column_value(self, row: Dict, field_type: str) -> Optional[str]:
        """Find a column value from row using field mappings."""
        possible_columns = self.FIELD_MAPPINGS.get(field_type, [])
        
        # First, try exact match with actual headers
        for col_name in self.headers:
            if col_name in possible_columns:
                value = row.get(col_name, '').strip()
                if value:
                    return value
        
        # Then try case-insensitive match
        for col_name in self.headers:
            for possible_col in possible_columns:
                if col_name.lower() == possible_col.lower():
                    value = row.get(col_name, '').strip()
                    if value:
                        return value
        
        return None
    
    def _parse_geometry(self, row: Dict) -> Optional[Point]:
        """Parse geometry from various CSV formats."""
        # Try to get from geom/geometry column (WKT format)
        geom_str = self._find_column_value(row, 'geom')
        if geom_str:
            try:
                # Try WKT format: "POINT(-117.1611 32.7157)"
                if 'POINT' in geom_str.upper():
                    coords = geom_str.upper().replace('POINT', '').replace('(', '').replace(')', '').strip()
                    lon, lat = map(float, coords.split())
                    return Point(lon, lat, srid=4326)
            except Exception as e:
                print(f"⚠️  Warning: Could not parse geometry from geom column: {e}")
        
        # Try to get from separate lat/lon columns
        lat_str = self._find_column_value(row, 'latitude')
        lon_str = self._find_column_value(row, 'longitude')
        
        if lat_str and lon_str:
            try:
                lat = float(lat_str)
                lon = float(lon_str)
                return Point(lon, lat, srid=4326)
            except ValueError as e:
                print(f"⚠️  Warning: Could not parse lat/lon: {e}")
                return None
        
        return None
    
    def _parse_hours(self, hours_str: str) -> Dict:
        """Parse hours from string into JSON format."""
        if not hours_str or hours_str.strip() == '':
            return {}
        
        # Try to parse as JSON
        try:
            parsed = json.loads(hours_str)
            if isinstance(parsed, dict):
                return parsed
        except (json.JSONDecodeError, ValueError):
            pass
        
        # If it's a simple string, return empty (can be enhanced later)
        return {}
    
    def _parse_tags(self, tags_str: str) -> List:
        """Parse tags from string into list."""
        if not tags_str or tags_str.strip() == '':
            return []
        
        # Try to parse as JSON
        try:
            parsed = json.loads(tags_str)
            if isinstance(parsed, list):
                return parsed
        except (json.JSONDecodeError, ValueError):
            pass
        
        # Try comma-separated
        if ',' in tags_str:
            return [tag.strip() for tag in tags_str.split(',') if tag.strip()]
        
        # Single tag
        return [tags_str.strip()]
    
    def _infer_resource_type(self, row: Dict) -> str:
        """Infer resource type from row data."""
        if self.default_resource_type:
            return self.default_resource_type
        
        # Check if there's an explicit rtype column
        rtype_value = self._find_column_value(row, 'rtype')
        if rtype_value:
            # Validate it's a known type
            valid_types = ['food', 'shelter', 'restroom', 'medical', 'legal', 'donation', 'other']
            if rtype_value.lower() in valid_types:
                return rtype_value.lower()
        
        # Check all text fields for keywords
        text_fields = []
        for key, value in row.items():
            if value and isinstance(value, str):
                text_fields.append(value)
        
        text_to_check = ' '.join(text_fields).lower()
        
        for rtype, keywords in self.TYPE_KEYWORDS.items():
            if any(keyword in text_to_check for keyword in keywords):
                return rtype
        
        return 'other'
    
    def parse_rows(self) -> List[Dict]:
        """Parse CSV rows into Resource-compatible dictionaries."""
        self.parsed_resources = []
        self.validation_errors = []
        
        for idx, row in enumerate(self.rows):
            try:
                # Extract required fields
                name = self._find_column_value(row, 'name')
                geom = self._parse_geometry(row)
                
                # Skip if missing required fields
                if not name:
                    self.validation_errors.append({
                        'index': idx,
                        'error': 'Missing required field: name',
                        'row': row
                    })
                    continue
                
                if not geom:
                    self.validation_errors.append({
                        'index': idx,
                        'error': 'Invalid or missing geometry (need lat/lon or geom)',
                        'name': name
                    })
                    continue
                
                # Parse hours_json
                hours_str = self._find_column_value(row, 'hours_json') or ''
                hours_json = self._parse_hours(hours_str)
                
                # Parse tags
                tags_str = self._find_column_value(row, 'tags') or ''
                tags = self._parse_tags(tags_str)
                
                # Build resource dict
                resource_data = {
                    'name': name,
                    'rtype': self._infer_resource_type(row),
                    'geom': geom,
                    'address': self._find_column_value(row, 'address') or '',
                    'phone': self._find_column_value(row, 'phone') or '',
                    'email': self._find_column_value(row, 'email') or '',
                    'website': self._find_column_value(row, 'website') or '',
                    'description': self._find_column_value(row, 'description') or '',
                    'state': 'visible',  # All new data will be visible during development
                    'tags': tags,
                    'hours_json': hours_json,
                    'raw_row': row,  # Store for reference
                }
                
                self.parsed_resources.append(resource_data)
                
            except Exception as e:
                self.validation_errors.append({
                    'index': idx,
                    'error': f'Parsing error: {str(e)}',
                    'row': row
                })
        
        return self.parsed_resources
    
    def preview(self, limit: int = 10) -> None:
        """Display a preview of parsed resources."""
        print("\n" + "="*80)
        print("IMPORT PREVIEW")
        print("="*80)
        
        print(f"\n📊 Statistics:")
        print(f"  • Total rows: {len(self.rows)}")
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
            if resource['email']:
                print(f"    Email: {resource['email']}")
            if resource['website']:
                print(f"    Website: {resource['website'][:60]}...")
            if resource.get('hours_json'):
                print(f"    Hours: {len(resource['hours_json'])} days configured")
            else:
                print(f"    Hours: Not available")
            if resource.get('tags'):
                print(f"    Tags: {', '.join(resource['tags'][:3])}")
        
        # Show validation errors
        if self.validation_errors:
            print(f"\n⚠️  Validation Errors (showing first 5):")
            print("-" * 80)
            for error in self.validation_errors[:5]:
                print(f"\nRow #{error.get('index', 'unknown')}:")
                print(f"  Error: {error['error']}")
                if 'name' in error:
                    print(f"  Name: {error['name']}")
        
        print("\n" + "="*80)
    
    def save_preview_to_file(self, output_path: str) -> None:
        """Save detailed preview to a JSON file for review."""
        resources_with_hours = sum(1 for r in self.parsed_resources if r.get('hours_json'))
        
        preview_data = {
            'import_date': datetime.now().isoformat(),
            'source_file': str(self.csv_path),
            'statistics': {
                'total_rows': len(self.rows),
                'parsed': len(self.parsed_resources),
                'errors': len(self.validation_errors),
                'resources_with_hours': resources_with_hours,
                'resources_without_hours': len(self.parsed_resources) - resources_with_hours,
            },
            'detected_columns': self.headers,
            'resources': [
                {
                    'name': r['name'],
                    'rtype': r['rtype'],
                    'address': r['address'],
                    'phone': r['phone'],
                    'email': r['email'],
                    'website': r['website'],
                    'description': r['description'],
                    'hours_json': r['hours_json'],
                    'tags': r['tags'],
                    'latitude': r['geom'].y,
                    'longitude': r['geom'].x,
                    'raw_row': r['raw_row'],
                }
                for r in self.parsed_resources
            ],
            'validation_errors': self.validation_errors,
        }
        
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
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
            print("❌ No resources to import. Run parse_rows() first.")
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
                # Remove raw_row before saving
                raw_row = resource_data.pop('raw_row', None)
                
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
        description='Import CSV data into Resource database',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Preview the import
  python import_csv.py data.csv --preview
  
  # Save preview to file (automatically saved in processed_data/)
  python import_csv.py data.csv --preview --output preview.json
  
  # Dry run (don't save to database)
  python import_csv.py data.csv --import --dry-run
  
  # Actually import
  python import_csv.py data.csv --import
  
  # Specify resource type (overrides CSV rtype column)
  python import_csv.py data.csv --type medical --import
        """
    )
    
    parser.add_argument('csv_file', help='Path to CSV file')
    parser.add_argument('--type', choices=['food', 'shelter', 'restroom', 'medical', 'legal', 'donation', 'other'],
                        help='Force all resources to this type (overrides CSV rtype column)')
    parser.add_argument('--preview', action='store_true', help='Show preview of data')
    parser.add_argument('--output', help='Save preview to JSON file (relative to processed_data/)')
    parser.add_argument('--import', dest='do_import', action='store_true', help='Import to database')
    parser.add_argument('--dry-run', action='store_true', help='Dry run (don\'t save to database)')
    parser.add_argument('--limit', type=int, default=10, help='Number of samples to show in preview')
    
    args = parser.parse_args()
    
    # Initialize importer
    importer = CSVImporter(args.csv_file, resource_type=args.type)
    
    # Load CSV
    if not importer.load_csv():
        sys.exit(1)
    
    # Parse rows
    importer.parse_rows()
    
    # Show preview
    if args.preview or not args.do_import:
        importer.preview(limit=args.limit)
        
        if args.output:
            # Save to processed_data directory
            script_dir = Path(__file__).parent
            processed_data_dir = script_dir / 'processed_data'
            output_path = processed_data_dir / args.output
            importer.save_preview_to_file(str(output_path))
    
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
