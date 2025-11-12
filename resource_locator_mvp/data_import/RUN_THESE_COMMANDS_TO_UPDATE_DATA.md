# ~900 Resource Data Update

These are the commands that you can run to update the database with approximately 900 new resources that cover most of the filter options in the UI. Starting at the root of the project:
- `cd resource_locator_mvp/data_import/`
- `python import_geojson.py raw_data/GeoJSON/Healthcare_Facilities.geojson --import`
- `python import_geojson.py raw_data/GeoJSON/Cool_Zones.geojson --import`
- `python3 import_csv.py raw_data/CSV/resource_data_food.csv --import`