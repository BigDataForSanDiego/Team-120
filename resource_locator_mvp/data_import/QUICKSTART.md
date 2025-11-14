# Import Pipeline Quick Start

## Step-by-Step: Importing Healthcare Facilities

### 1. Preview the Data (2 minutes)

```bash
cd /home/robert/Team-120/data_import
python import_geojson.py raw_data/GeoJSON/Healthcare_Facilities.geojson --preview
```

**Look for:**
- ✅ How many features loaded successfully?
- ✅ Resource type distribution (should be mostly "medical")
- ✅ Sample resources - do names look correct?
- ❌ Any validation errors?

### 2. Save Detailed Preview (1 minute)

```bash
python import_geojson.py raw_data/GeoJSON/Healthcare_Facilities.geojson \
  --preview \
  --output preview_healthcare.json
```

**Review `preview_healthcare.json`:**
- Check `statistics` section
- Browse through `resources` array
- Look at `raw_properties` to see what other fields are available
- Check `validation_errors` array

### 3. Dry Run (1 minute)

```bash
python import_geojson.py raw_data/GeoJSON/Healthcare_Facilities.geojson \
  --type medical \
  --import \
  --dry-run
```

This shows what **would** be created without actually saving anything.

### 4. Import (1 minute)

```bash
python import_geojson.py raw_data/GeoJSON/Healthcare_Facilities.geojson \
  --type medical \
  --import
```

Type `y` when prompted to confirm.

### 5. Review in Admin (5 minutes)

1. Go to http://127.0.0.1:8000/admin/resources/resource/
2. Filter by **State: Not Visible**
3. Review imported resources
4. Edit any that need corrections
5. Change state to **Visible** to publish

## Common Commands

```bash
# Preview with auto-detected types
python import_geojson.py data.geojson --preview

# Preview with forced type
python import_geojson.py data.geojson --type medical --preview

# Save detailed preview
python import_geojson.py data.geojson --preview --output preview.json

# Dry run
python import_geojson.py data.geojson --import --dry-run

# Actual import
python import_geojson.py data.geojson --import

# Force type on import
python import_geojson.py data.geojson --type shelter --import
```

## Checking Import Results

### Command Line

```bash
# Count imported resources
cd /home/robert/Team-120/resource_locator_mvp
python manage.py shell

>>> from resources.models import Resource
>>> Resource.objects.filter(state='not_visible').count()
>>> Resource.objects.filter(rtype='medical').count()
```

### Django Admin

1. Go to http://127.0.0.1:8000/admin/
2. Login with your superuser credentials
3. Navigate to **Resources** → **Resources**
4. Use filters:
   - **State: Not Visible** (new imports)
   - **Resource Type: Medical** (specific type)
5. Click any resource to edit on the map

### API Check

```bash
# Check total visible resources
curl http://127.0.0.1:8000/api/resources/ | python -m json.tool | grep -c "Feature"

# Check medical resources
curl "http://127.0.0.1:8000/api/resources/?rtype=medical" | python -m json.tool
```

## Safety Features

✅ All imports start as `state='not_visible'` (hidden from public)
✅ Duplicate detection (name + location within 100m)
✅ Dry run mode available
✅ Confirmation prompt before import
✅ Preview shows validation errors
✅ Can review preview JSON before importing

## Next: Process More Files

Once you're comfortable with the workflow:

```bash
# Import multiple files
python import_geojson.py raw_data/GeoJSON/file1.geojson --import
python import_geojson.py raw_data/GeoJSON/file2.geojson --import
python import_geojson.py raw_data/GeoJSON/file3.geojson --import

# Batch review in admin
# Filter by state='not_visible' and created_at=today
```