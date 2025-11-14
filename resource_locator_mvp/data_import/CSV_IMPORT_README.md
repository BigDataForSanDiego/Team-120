# CSV Import Script Documentation

## Overview

The `import_csv.py` script provides a flexible way to import resource data from CSV files into the Resource Locator database. It follows the same two-stage safety process as the GeoJSON importer:

1. **Preview & Validate**: Analyze data without modifying the database
2. **Import**: Save validated resources to the database

## Quick Start

### 1. Preview Your CSV Data

```bash
cd data_import
python3 import_csv.py raw_data/CSV/resource_data_masterfile.csv --preview
```

This will show:
- Statistics (total rows, parsed successfully, errors, hours availability)
- Detected column names
- Resource type distribution
- Sample resources with parsed fields
- Validation errors

### 2. Save Detailed Preview

```bash
python3 import_csv.py raw_data/CSV/resource_data_masterfile.csv \
  --preview \
  --output resource_preview.json
```

Preview files are automatically saved to `processed_data/` directory.

### 3. Dry Run Import

```bash
python3 import_csv.py raw_data/CSV/resource_data_masterfile.csv \
  --import \
  --dry-run
```

This simulates the import without saving to the database.

### 4. Actual Import

```bash
python3 import_csv.py raw_data/CSV/resource_data_masterfile.csv --import
```

You'll be prompted to confirm before any changes are made.

## Command Line Options

```
usage: import_csv.py [-h] [--type {food,shelter,restroom,medical,legal,donation,other}]
                     [--preview] [--output OUTPUT] [--import] [--dry-run]
                     [--limit LIMIT]
                     csv_file

positional arguments:
  csv_file              Path to CSV file

optional arguments:
  --type TYPE           Force all resources to this type (overrides CSV rtype column)
  --preview             Show preview of data
  --output OUTPUT       Save preview to JSON file (relative to processed_data/)
  --import              Import to database
  --dry-run            Dry run (don't save to database)
  --limit LIMIT        Number of samples to show in preview (default: 10)
```

## Column Mapping

The importer automatically detects and maps various column name formats:

| Resource Field | Possible CSV Column Names |
|---------------|---------------------------|
| `name` | name, NAME, Name, facility_name, organization, Organization |
| `rtype` | **rtype**, type, resource_type, category, Category |
| `address` | address, ADDRESS, Address, street_address, location |
| `phone` | phone, PHONE, Phone, telephone, contact_phone |
| `email` | email, EMAIL, Email, contact_email |
| `website` | website, WEBSITE, Website, url, URL, web_address |
| `description` | description, DESCRIPTION, Description, notes, comments |
| `hours_json` | hours_json, hours, Hours, operating_hours |
| `tags` | tags, Tags, TAGS, keywords |
| `latitude` | lat, Lat, LAT, latitude, Latitude, LATITUDE |
| `longitude` | lon, Long, LONG, longitude, Longitude, lng |
| `geom` | geom, geometry, wkt, point |

**Note**: Column matching is **case-insensitive** and tries exact matches first.

## Resource Type Handling

### Explicit rtype Column (Recommended)

If your CSV has an `rtype` column, the script will use its values by default:

```csv
name,rtype,address,lat,lon
"Community Center","shelter","123 Main St",32.7157,-117.1611
"Health Clinic","medical","456 Oak Ave",32.7257,-117.1411
```

Valid rtype values: `food`, `shelter`, `restroom`, `medical`, `legal`, `donation`, `other`

### Auto-Detection (Fallback)

If no `rtype` column exists, or for rows with empty/invalid rtype values, the script uses keyword detection similar to the GeoJSON importer.

### Override with --type Flag

Force all resources to a specific type:

```bash
python3 import_csv.py data.csv --type shelter --import
```

This overrides both CSV rtype column and auto-detection.

## Geometry Handling

The script supports multiple geometry formats:

### 1. Separate Lat/Lon Columns (Most Common)

```csv
name,Lat,Long
"Resource Name",32.7157,-117.1611
```

Column names: `lat`, `Lat`, `latitude`, `lon`, `Long`, `longitude`, etc.

### 2. WKT Geometry Column

```csv
name,geom
"Resource Name","POINT(-117.1611 32.7157)"
```

Column names: `geom`, `geometry`, `wkt`, `point`

**Note**: Coordinates should be in WGS84 (EPSG:4326) format.

## Hours of Operation

The script attempts to parse hours from the `hours_json` or `hours` column:

### JSON Format (Recommended)

```csv
name,hours_json
"Library","{\"mon\":[[\"09:00\",\"17:00\"]],\"tue\":[[\"09:00\",\"17:00\"]]}"
```

### Empty/Unparseable

If hours cannot be parsed, `hours_json` is set to `{}` (empty object), which is valid and indicates "hours not available."

## Tags

Tags can be provided as:

### JSON Array

```csv
name,tags
"Resource","[\"food pantry\",\"emergency\"]"
```

### Comma-Separated

```csv
name,Tags
"Resource","food pantry, emergency, walk-up"
```

### Single Tag

```csv
name,tags
"Resource","emergency"
```

## File Encoding

The script automatically handles various file encodings:
- UTF-8 (preferred)
- Latin-1
- CP1252
- ISO-8859-1

If a file cannot be read with UTF-8, the script tries alternative encodings automatically.

## Validation Errors

Common validation errors and solutions:

### "Missing required field: name"

**Cause**: No name column found or empty name value

**Solution**: 
- Ensure CSV has a column named `name`, `NAME`, `Name`, etc.
- Check that the name field is not empty

### "Invalid or missing geometry"

**Cause**: Cannot find or parse coordinates

**Solution**:
- Ensure CSV has either:
  - `Lat`/`Long` columns with numeric values
  - `geom` column with WKT format: `POINT(lon lat)`
- Check for empty values in geometry columns
- Verify coordinates are in decimal degrees (not DMS format)

## Example Workflow

```bash
# 1. Preview the data
python3 import_csv.py raw_data/CSV/my_data.csv --preview --limit 20

# 2. Save detailed preview for review
python3 import_csv.py raw_data/CSV/my_data.csv \
  --preview \
  --output my_data_preview.json

# 3. Review processed_data/my_data_preview.json
# Look for:
#   - Are names extracted correctly?
#   - Are resource types correct?
#   - Any validation errors?
#   - Are coordinates valid?

# 4. Do a dry run
python3 import_csv.py raw_data/CSV/my_data.csv \
  --import \
  --dry-run

# 5. If dry run looks good, import for real
python3 import_csv.py raw_data/CSV/my_data.csv --import

# 6. Review in Django admin
# http://127.0.0.1:8000/admin/resources/resource/
# Filter by state='visible' to see new imports
```

## Duplicate Detection

The importer checks for existing resources by:
- Exact name match
- Location within 100 meters

Duplicates are automatically skipped.

## Differences from GeoJSON Importer

| Feature | GeoJSON | CSV |
|---------|---------|-----|
| Geometry format | Built-in Point | Lat/Long or WKT |
| Resource type | Auto-detect or --type | CSV column, auto-detect, or --type |
| Hours parsing | Multi-line format supported | JSON format only |
| Preview output | Same directory | `processed_data/` directory |
| Field detection | Fixed property names | Flexible column matching |

## Tips for Best Results

1. **Use consistent column names**: Match the expected names in the mapping table
2. **Include rtype column**: Explicitly specify resource types to avoid misclassification
3. **Provide lat/lon**: Easier than WKT format
4. **Test with preview first**: Always preview before importing
5. **Check validation errors**: Review errors in preview output
6. **Use descriptive filenames**: Makes preview files easier to identify

## Next Steps

After importing:
1. Go to Django admin: http://127.0.0.1:8000/admin/resources/resource/
2. Filter by recent creation date
3. Review imported resources
4. Make any necessary edits
5. Resources are automatically `state='visible'` during development

## Troubleshooting

### Import shows 0 parsed resources

- Check CSV format (comma-separated, proper headers)
- Verify file encoding
- Ensure required columns exist (name + geometry)

### All resources classified as "other"

- Add explicit `rtype` column to CSV
- Or use `--type` flag to force type
- Check keyword detection matches your data

### Geometry errors

- Verify lat/lon values are decimal numbers
- Check coordinate order (latitude, longitude)
- Ensure coordinates are within valid ranges (-90 to 90 for lat, -180 to 180 for lon)
