# 🚀 Getting Started - GeoDjango Demo

## For Team Members - Start Here!

This is your **one-page guide** to get the GeoDjango demo running in 5 minutes.

## What Is This?

A complete Django + GeoDjango + DRF demo application that shows how to build geospatial web apps. It includes:
- 🗺️ Interactive maps with Leaflet
- 📍 12 pre-loaded San Diego locations
- 🔌 RESTful GeoJSON API
- 🛠️ Admin interface with map widgets
- 📱 Mobile-friendly responsive design

## 3 Ways to Get Started

### Option 1: Automated Setup (Recommended)
```bash
cd geodjango_demo
./setup.sh
```
Follow the prompts. Done! 🎉

### Option 2: Manual Setup (5 commands)
```bash
cd geodjango_demo
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your database credentials
python manage.py migrate
python manage.py createsuperuser
python manage.py load_sample_data
python manage.py runserver
```

### Option 3: Docker (Coming Soon)
Docker Compose setup coming in next iteration.

## Prerequisites

**Must Have:**
- Python 3.10+
- PostgreSQL 14+ with PostGIS
- GDAL libraries

**Quick Install (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install python3-pip python3-venv postgresql postgis gdal-bin libgdal-dev
```

**Quick Install (macOS):**
```bash
brew install postgresql postgis gdal
```

## First Time Setup

### 1. Database Setup (One Time)
```bash
# Create database
createdb geodjango_db

# Enable PostGIS
psql geodjango_db -c "CREATE EXTENSION postgis;"
```

### 2. Configure Environment
```bash
# Copy example
cp .env.example .env

# Edit with your favorite editor
nano .env  # or code .env or vim .env
```

Required settings in `.env`:
```env
DB_NAME=geodjango_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### 3. Run Migrations
```bash
python manage.py migrate
```

### 4. Create Admin User
```bash
python manage.py createsuperuser
```

### 5. Load Sample Data
```bash
python manage.py load_sample_data
```

### 6. Start Server
```bash
python manage.py runserver
```

## Access Points

Once running, visit:

| What | URL |
|------|-----|
| 🏠 Home Page | http://localhost:8000/ |
| ✏️ Create Waypoint | http://localhost:8000/create/ |
| 🗺️ Map View | http://localhost:8000/map/ |
| 🛠️ Admin Interface | http://localhost:8000/admin/ |
| 🔌 API (GeoJSON) | http://localhost:8000/api/waypoints/ |
| 📍 Nearby API | http://localhost:8000/api/waypoints/nearby/?lat=32.7157&lon=-117.1611&distance=5 |

## Quick Tour (2 minutes)

### 1. View Home Page
- See list of waypoints
- Click category buttons to filter
- Notice no page reload (Alpine.js)

### 2. Create a Waypoint
- Go to http://localhost:8000/create/
- Fill in name, category, description
- Click on map to set location
- Submit form

### 3. View Map
- Go to http://localhost:8000/map/
- See all waypoints as markers
- Click markers for info
- Filter by category

### 4. Try the API
- Visit http://localhost:8000/api/waypoints/
- See GeoJSON format
- Try filtering: `/api/waypoints/?category=park`
- Try nearby search: `/api/waypoints/nearby/?lat=32.7157&lon=-117.1611&distance=5`

### 5. Use Admin
- Login at http://localhost:8000/admin/
- Click "Waypoints"
- Try editing a waypoint
- Click map to change location

## Common Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Run development server
python manage.py runserver

# Create migrations (after model changes)
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load sample data
python manage.py load_sample_data

# Django shell (for testing)
python manage.py shell

# Check for issues
python manage.py check
```

## Troubleshooting

### Can't connect to database
```bash
# Check PostgreSQL is running
sudo systemctl status postgresql  # Linux
brew services list                # macOS

# Check database exists
psql -l | grep geodjango_db
```

### PostGIS not found
```bash
# Enable PostGIS extension
psql geodjango_db -c "CREATE EXTENSION postgis;"
```

### Import errors
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Map not loading
- Check browser console (F12) for JavaScript errors
- Verify internet connection (Leaflet loads from CDN)
- Clear browser cache

## Documentation

For more details, see:

| Document | Purpose |
|----------|---------|
| **README.md** | Complete setup guide (start here for full details) |
| **QUICKSTART.md** | This file - quick reference |
| **ARCHITECTURE.md** | Technical deep-dive, architecture diagrams |
| **STRUCTURE.md** | Visual diagrams of project structure |
| **CHECKLIST.md** | Step-by-step verification checklist |
| **PROJECT_SUMMARY.md** | Project overview and statistics |

## File Structure (Quick Reference)

```
geodjango_demo/
├── manage.py              # Django CLI
├── requirements.txt       # Dependencies
├── .env                   # Your config (not in git)
├── setup.sh              # Automated setup
│
├── geodjango_demo/       # Project config
│   ├── settings.py       # Django settings
│   └── urls.py          # URL routing
│
├── waypoints/           # Main app
│   ├── models.py        # Waypoint model
│   ├── views.py         # Views & API
│   ├── serializers.py   # DRF serializers
│   ├── forms.py         # Django forms
│   └── admin.py         # Admin config
│
└── templates/           # HTML templates
    ├── base.html
    └── waypoints/
        ├── waypoint_list.html
        ├── waypoint_create.html
        └── waypoint_map.html
```

## Key Concepts

### Models (waypoints/models.py)
```python
class Waypoint(models.Model):
    location = models.PointField(geography=True)  # PostGIS point
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
```

### API (waypoints/views.py)
```python
class WaypointViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Waypoint.objects.all()
    serializer_class = WaypointSerializer  # GeoJSON output
```

### Templates (templates/waypoints/)
- Server-side rendering with Django templates
- HTMX for progressive enhancement
- Alpine.js for reactive UI
- Leaflet for maps

## Next Steps

1. ✅ Get it running (you are here!)
2. 📖 Read the code in `waypoints/models.py`
3. 🔍 Explore the API endpoints
4. 🎨 Customize the templates
5. 🚀 Add your own features

## Quick Tips

- **Development:** Always activate venv first
- **Database:** PostgreSQL must be running
- **Static Files:** Served automatically in development
- **Debug Mode:** Enabled by default in `.env`
- **API Format:** Always returns GeoJSON for geospatial data

## Learn More

- **Django Tutorial:** https://docs.djangoproject.com/en/stable/intro/tutorial01/
- **GeoDjango Tutorial:** https://docs.djangoproject.com/en/stable/ref/contrib/gis/tutorial/
- **DRF Tutorial:** https://www.django-rest-framework.org/tutorial/quickstart/
- **Leaflet Docs:** https://leafletjs.com/reference.html

## Need Help?

1. Check **CHECKLIST.md** for verification steps
2. Read **README.md** for detailed explanations
3. Review **ARCHITECTURE.md** for technical details
4. Search for error message online
5. Check Django/GeoDjango documentation

## Success!

If you can:
- ✅ See the home page
- ✅ Create a waypoint
- ✅ View the map
- ✅ Access the API
- ✅ Login to admin

**You're all set!** 🎉

Now explore the code and build something awesome!

---

**Tech Stack:** Django 5.x | GeoDjango | DRF | PostGIS | Leaflet | HTMX | Alpine.js

**For:** Team 120 - BDA Hackathon 2025
