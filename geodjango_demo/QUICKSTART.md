# Quick Start Guide

## For Team Members

This is a Django + GeoDjango + DRF demo application that demonstrates how to build geospatial web applications.

### What This Demo Shows

1. **GeoDjango Setup:** How to configure Django for geospatial data
2. **PostGIS Integration:** Using PostgreSQL with PostGIS for spatial queries
3. **REST API:** Building GeoJSON APIs with Django REST Framework
4. **Interactive Maps:** Using Leaflet for map visualization and user input
5. **Admin Interface:** Built-in admin with map widgets
6. **Thin Client UI:** HTMX + Alpine.js for minimal JavaScript footprint

### Three User Interfaces

1. **List View** (`/`) - Browse waypoints with category filtering
2. **Create Form** (`/create/`) - Add new waypoints with map picker
3. **Map View** (`/map/`) - See all waypoints on an interactive map

### API Endpoints

- `GET /api/waypoints/` - List all waypoints (GeoJSON format)
- `GET /api/waypoints/?category=park` - Filter by category
- `GET /api/waypoints/nearby/?lat=32.7157&lon=-117.1611&distance=5` - Find nearby waypoints

### Quick Setup (5 minutes)

1. **Install dependencies:**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Set up database:**
   ```bash
   # Create PostgreSQL database with PostGIS
   createdb geodjango_db
   psql geodjango_db -c "CREATE EXTENSION postgis;"
   ```

3. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. **Start server:**
   ```bash
   python manage.py runserver
   ```

6. **Visit:**
   - App: http://localhost:8000/
   - Admin: http://localhost:8000/admin/
   - API: http://localhost:8000/api/waypoints/

### Key Files to Review

- `waypoints/models.py` - Waypoint model with GeoDjango PointField
- `waypoints/serializers.py` - DRF serializers for GeoJSON output
- `waypoints/views.py` - API viewsets and template views
- `geodjango_demo/settings.py` - Django settings with GeoDjango config
- `templates/` - Django templates with Leaflet integration

### Demo Data

Use the admin interface or create form to add sample waypoints:
- Museums in San Diego
- Parks and recreation areas
- Restaurants
- Transit stations

### Questions?

See the full README.md for detailed documentation.

---

**Tech Stack:** Django 5.x | GeoDjango | DRF | PostGIS | Leaflet | HTMX | Alpine.js
