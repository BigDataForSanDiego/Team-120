# Data Import Pipeline

This directory contains tools for importing external data sources (GeoJSON, CSV) into the Resource Locator database.

## Overview

The import pipeline provides a **safe, two-stage process**:

1. **Preview & Validate**: Analyze the data without modifying the database
2. **Import**: Save validated resources to the database

All imported resources start with `state='not_visible'` (see note below) so they can be reviewed before being made public.

NOTE: During developemnt, all new resources will start as `state='visible'` to enable UI testing.

## Quick Start

### 1. Preview Your Data

```bash
cd data_import
python import_geojson.py raw_data/GeoJSON/Healthcare_Facilities.geojson --preview
```

This will show:
- Statistics (total features, parsed successfully, errors, hours availability)
- Resource type distribution
- Sample resources with their parsed fields (including hours status)
- Validation errors

### 2. Save Detailed Preview

```bash
python import_geojson.py raw_data/GeoJSON/Healthcare_Facilities.geojson \
  --preview \
  --output preview_healthcare.json
```

Review the `preview_healthcare.json` file to see:
- All parsed resources with their fields (including `hours_json`)
- Statistics on hours availability
- Raw properties from the GeoJSON
- Complete validation errors
- Geographic coordinates

### 3. Dry Run Import

```bash
python import_geojson.py raw_data/GeoJSON/Healthcare_Facilities.geojson \
  --import \
  --dry-run
```

This simulates the import without saving to the database.

### 4. Actual Import

```bash
python import_geojson.py raw_data/GeoJSON/Healthcare_Facilities.geojson --import
```

You'll be prompted to confirm before any changes are made.

## Command Line Options

```
usage: import_geojson.py [-h] [--type {food,shelter,restroom,medical,legal,donation,other}]
                         [--preview] [--output OUTPUT] [--import] [--dry-run]
                         [--limit LIMIT]
                         geojson_file

positional arguments:
  geojson_file          Path to GeoJSON file

optional arguments:
  --type TYPE           Force all resources to this type (otherwise auto-detected)
  --preview             Show preview of data
  --output OUTPUT       Save preview to JSON file
  --import              Import to database
  --dry-run            Dry run (don't save to database)
  --limit LIMIT        Number of samples to show in preview (default: 10)
```

## Field Mapping

The importer automatically maps common field names to Resource model fields:

| Resource Field | Possible GeoJSON Fields |
|---------------|-------------------------|
| `name` | name, NAME, facility_name, FACILITY_NAME, site_name, SITE_NAME, Organization |
| `address` | address, ADDRESS, street_address, STREET_ADDRESS, location, DBA_ADDRESS1, ADDR |
| `city` | city, CITY, DBA_CITY |
| `zip_code` | zip_code, ZIP_CODE, zipcode, ZIPCODE, DBA_ZIP_CODE, postal_code |
| `phone` | phone, PHONE, telephone, TELEPHONE, contact_phone, CONTACT_PHONE |
| `website` | website, WEBSITE, url, URL, web_address, WEB_ADDRESS |
| `description` | description, DESCRIPTION, notes, NOTES, comments, COMMENTS |
| `hours` | hours, HOURS, hours_of_operation, HOURS_OF_OPERATION, operating_hours, OPERATING_HOURS |

### Address Construction

If a complete address isn't found, the importer will construct one from separate city and zip code fields.

### Hours of Operation

The importer extracts hours information and converts it to the expected format: `{"mon":[[\"09:00\",\"17:00\"]], "tue":...}`

**Supported hours formats:**
- **24/7 or Always Open**: Creates a full 7-day schedule with 00:00-23:59
- **JSON format**: Directly uses the provided JSON structure
- **Multi-line format**: Parses newline-separated daily schedules
  - Example: `"Mon 12:00pm-8:00pm\nTues 12:00pm-8:00pm\nWed Closed"`
  - Automatically converts 12-hour times to 24-hour format
  - Handles "Closed" entries as empty arrays
  - Skips non-schedule lines (like "Observed Holidays")
- **Empty/Not available**: Sets `hours_json` to `{}` (empty object)

**Examples of parsed formats:**

1. **Multi-line with varied hours:**
   ```
   Mon 12:00pm-8:00pm
   Tues 12:00pm-8:00pm
   Wed 12:00pm-8:00pm
   Thurs 12:00pm-8:00pm
   Fri 12:00pm-5:00pm
   Sat Closed
   Sun Closed
   ```
   Result: Mon-Thu (12:00-20:00), Fri (12:00-17:00), Sat-Sun (closed)

2. **24/7 service:**
   ```
   24/7
   ```
   Result: All days (00:00-23:59)

Resources without hours information will have an empty `hours_json` field, which is valid and indicates that hours are not available.

## Resource Type Detection

If you don't specify `--type`, the importer tries to auto-detect the resource type based on keywords:

- **medical**: hospital, clinic, health, medical, doctor, physician, healthcare, care center, emergency, urgent care, surgery
- **food**: food, meal, pantry, kitchen, soup, nutrition
- **shelter**: shelter, housing, homeless, transitional
- **legal**: legal, law, attorney, court
- **restroom**: restroom, bathroom, toilet, washroom
- **donation**: donation, thrift, goodwill, charity

Resources that don't match any keywords are classified as **other**.

## Import States

All imported resources have `state='not_visible'` by default (see note below). This allows you to:

1. Review them in the Django admin
2. Edit fields as needed
3. Change state to `'visible'` when ready

NOTE: During developemnt, all new resources will start as `state='visible'` to enable UI testing.

## Duplicate Detection

The importer checks for existing resources by:
- Exact name match
- Location within 100 meters

Duplicates are automatically skipped.

## Workflow Example

```bash
# 1. Preview the data
python import_geojson.py raw_data/GeoJSON/Healthcare_Facilities.geojson --preview --limit 20

# 2. Save detailed preview for review
python import_geojson.py raw_data/GeoJSON/Healthcare_Facilities.geojson \
  --preview \
  --output preview_healthcare.json

# 3. Review preview_healthcare.json
# Look for:
#   - Are names extracted correctly?
#   - Are addresses present?
#   - Are resource types correct?
#   - Any validation errors?

# 4. If preview looks good, do a dry run
python import_geojson.py raw_data/GeoJSON/Healthcare_Facilities.geojson \
  --import \
  --dry-run

# 5. If dry run looks good, import for real
python import_geojson.py raw_data/GeoJSON/Healthcare_Facilities.geojson --import

# 6. Go to Django admin and review the imported resources
# http://127.0.0.1:8000/admin/resources/resource/
# Filter by state='not_visible' to see new imports

# 7. Make any necessary edits in admin

# 8. Change state to 'visible' to publish them
```

## Troubleshooting

### "No resources to import"
- Check that the GeoJSON file has a `"type": "FeatureCollection"` at the root
- Ensure features have both `properties` and `geometry` objects

### "Missing required field: name"
- The importer couldn't find a name field
- Check your GeoJSON properties and update `FIELD_MAPPINGS` in the script if needed

### "Invalid or missing geometry"
- Ensure geometries are of type "Point" (not Polygon or MultiPoint)
- Check that coordinates are in [longitude, latitude] order

### Import fails with geometry errors
- Coordinates should be in EPSG:4326 (WGS84) format
- Longitude should be between -180 and 180
- Latitude should be between -90 and 90

## Next Steps

- [ ] Extend to support CSV files
- [ ] Add address geocoding for files without coordinates
- [ ] Add field mapping configuration file
- [ ] Add support for extracting hours from structured fields
- [ ] Add batch import from multiple files