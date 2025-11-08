# GeoDjango Demo Application

A full-featured demonstration of Django + GeoDjango + Django REST Framework (DRF) for geospatial web applications.

---

## ⚡ QUICK LAUNCH (No Database Setup!)

**Want to see it running in 2 minutes?** We now support SQLite/SpatiaLite for instant demo!

```bash
cd geodjango_demo
./quickstart.sh
```

Then visit: http://localhost:8000/

👉 **See [LAUNCH.md](LAUNCH.md) for the super-fast setup guide!**

The rest of this README covers the full PostgreSQL setup for production use.

---

## 🧱 Tech Stack

- **Backend Framework:** Django 5.x
- **Geospatial Extension:** GeoDjango with PostGIS
- **REST API:** Django REST Framework (DRF) + DRF-GIS
- **Database:** PostgreSQL with PostGIS extension
- **Frontend:**
  - Django Templates
  - HTMX (lightweight interactivity)
  - Alpine.js (reactive UI)
  - Leaflet (interactive maps)
  - Tailwind CSS (styling)

## 🎯 Features

### 1. **Geospatial Data Management**
- Store waypoints with geographic coordinates using GeoDjango's `PointField`
- PostGIS backend for efficient spatial queries
- Distance-based queries (`ST_DWithin`, `ST_DistanceSphere`)

### 2. **RESTful API (GeoJSON)**
- List all waypoints in GeoJSON format
- Filter by category
- Find nearby waypoints within a specified radius
- Full CRUD operations via API

### 3. **User Interfaces**
- **Home Page:** List view with category filtering (Alpine.js)
- **Create Page:** Form with interactive Leaflet map picker
- **Map View:** Full interactive map with all waypoints
- **Admin Dashboard:** Django admin with geospatial widgets

### 4. **Admin Interface**
- Built-in Django admin with GIS widgets
- Map-based editing for location fields
- Search, filter, and CRUD operations

## 📋 Prerequisites

### System Requirements
- Python 3.10 or higher
- PostgreSQL 14+ with PostGIS extension
- GDAL/GEOS libraries

### Install System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install python3-pip python3-venv postgresql postgresql-contrib postgis gdal-bin libgdal-dev
```

**macOS (using Homebrew):**
```bash
brew install postgresql postgis gdal
```

**Windows:**
- Install PostgreSQL from https://www.postgresql.org/download/windows/
- Install PostGIS from https://postgis.net/install/
- Install GDAL from OSGeo4W: https://trac.osgeo.org/osgeo4w/

## 🚀 Quick Start

### 1. Clone or Navigate to Project
```bash
cd geodjango_demo
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up PostgreSQL Database

**Create Database:**
```bash
sudo -u postgres psql
```

Then in PostgreSQL:
```sql
CREATE DATABASE geodjango_db;
CREATE USER postgres WITH PASSWORD 'yourpassword';
ALTER ROLE postgres SET client_encoding TO 'utf8';
ALTER ROLE postgres SET default_transaction_isolation TO 'read committed';
ALTER ROLE postgres SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE geodjango_db TO postgres;
\c geodjango_db
CREATE EXTENSION postgis;
\q
```

### 5. Configure Environment Variables
```bash
cp .env.example .env
```

Edit `.env` with your database credentials:
```env
DB_NAME=geodjango_db
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 6. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create Superuser (for Admin Access)
```bash
python manage.py createsuperuser
```

### 8. Run Development Server
```bash
python manage.py runserver
```

The application will be available at:
- **Home:** http://localhost:8000/
- **Admin:** http://localhost:8000/admin/
- **API:** http://localhost:8000/api/waypoints/
- **Map View:** http://localhost:8000/map/

## 📁 Project Structure

```
geodjango_demo/
├── geodjango_demo/           # Main project configuration
│   ├── __init__.py
│   ├── settings.py           # Django settings with GeoDjango config
│   ├── urls.py               # URL routing
│   ├── wsgi.py               # WSGI config for deployment
│   └── asgi.py               # ASGI config for async
├── waypoints/                # Main app for waypoint management
│   ├── models.py             # Waypoint model with PointField
│   ├── serializers.py        # DRF serializers (GeoJSON)
│   ├── views.py              # API viewsets and template views
│   ├── forms.py              # Django forms
│   └── admin.py              # Admin configuration with GIS widgets
├── templates/                # Django templates
│   ├── base.html             # Base template with nav and footer
│   └── waypoints/
│       ├── waypoint_list.html    # Home page
│       ├── waypoint_create.html  # Form with map picker
│       └── waypoint_map.html     # Interactive map view
├── static/                   # Static files (CSS, JS)
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
└── .env.example              # Environment variables template
```

## 🔌 API Endpoints

### Base URL: `/api/waypoints/`

#### List All Waypoints (GeoJSON)
```
GET /api/waypoints/
```

Response:
```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [-117.1611, 32.7157]
      },
      "properties": {
        "id": 1,
        "name": "Balboa Park",
        "category": "park",
        "description": "Beautiful urban park in San Diego",
        "created_at": "2025-11-08T12:00:00Z"
      }
    }
  ]
}
```

#### Filter by Category
```
GET /api/waypoints/?category=restaurant
```

#### Find Nearby Waypoints
```
GET /api/waypoints/nearby/?lat=32.7157&lon=-117.1611&distance=5
```

Parameters:
- `lat` (required): Latitude
- `lon` (required): Longitude
- `distance` (optional): Radius in kilometers (default: 5)

## 📊 Data Model

### Waypoint Model
```python
class Waypoint(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    location = models.PointField(geography=True)  # GeoDjango field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

**Categories:**
- Restaurant
- Park
- Museum
- Landmark
- Hotel
- Transit Station
- Other

## 🎨 Frontend Architecture

### Thin Client Approach
Following the Notion stack guidelines, this demo uses a "thin client" architecture:

1. **Server-Side Rendering:** Django templates for initial page load
2. **Progressive Enhancement:** HTMX for dynamic updates without full page reloads
3. **Minimal JavaScript:** Alpine.js for reactive UI components (filtering, form state)
4. **Map Integration:** Leaflet for interactive map functionality

### Benefits
- Fast initial load times
- Works on low-power mobile devices
- SEO-friendly
- Progressive enhancement strategy

## 🚢 Deployment

### Recommended Hosting Options

**Backend:**
- Render.com
- Fly.io
- Railway.app
- Heroku

**Database:**
- Supabase (PostgreSQL + PostGIS)
- Neon.tech
- Crunchy Bridge
- AWS RDS

### Production Settings

1. **Update `.env` for production:**
```env
DEBUG=False
ALLOWED_HOSTS=your-domain.com
SECRET_KEY=generate-a-strong-secret-key
```

2. **Collect static files:**
```bash
python manage.py collectstatic
```

3. **Use Gunicorn for production:**
```bash
gunicorn geodjango_demo.wsgi:application --bind 0.0.0.0:8000
```

4. **Set up Nginx as reverse proxy (optional)**

### Environment Variables for Production
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: Django secret key
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts
- `DEBUG`: Set to `False`

## 🧪 Testing the Application

### Add Sample Data via Admin
1. Go to http://localhost:8000/admin/
2. Log in with your superuser credentials
3. Click "Waypoints" → "Add Waypoint"
4. Click on the map to select a location
5. Fill in name, category, and description
6. Save

### Add Sample Data via Web Form
1. Go to http://localhost:8000/create/
2. Fill in the form
3. Click on the map to select a location
4. Submit

### View Data
- **List View:** http://localhost:8000/
- **Map View:** http://localhost:8000/map/
- **API (GeoJSON):** http://localhost:8000/api/waypoints/

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [GeoDjango Documentation](https://docs.djangoproject.com/en/stable/ref/contrib/gis/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostGIS Documentation](https://postgis.net/documentation/)
- [Leaflet Documentation](https://leafletjs.com/)

## 🎯 Key Demonstration Features

This demo showcases:

1. ✅ **GeoDjango Integration:** PointField with PostGIS backend
2. ✅ **GeoJSON API:** RESTful endpoints with DRF-GIS
3. ✅ **Interactive Maps:** Leaflet for user input and visualization
4. ✅ **Admin Interface:** Built-in GIS widgets for data management
5. ✅ **Thin Client UI:** HTMX + Alpine.js for minimal JavaScript
6. ✅ **Spatial Queries:** Distance-based filtering
7. ✅ **Category Filtering:** Dynamic UI without page reloads
8. ✅ **Production Ready:** Environment configuration and deployment guidance

## 🤝 Contributing

This is a demonstration project for the BDA Hackathon 2025. Feel free to extend it with additional features!

## 📄 License

MIT License - feel free to use this as a starting point for your projects.

---

Built with ❤️ using Django + GeoDjango + DRF
