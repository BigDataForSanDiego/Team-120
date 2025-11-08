# ⚡ Quick Launch Guide - Simplified Setup!

This demo now uses **SQLite with SpatiaLite** instead of PostgreSQL, making setup much faster!

## 📋 Prerequisites (One-Time Setup)

GeoDjango requires GDAL libraries. Install them first:

### Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install gdal-bin libgdal-dev libsqlite3-mod-spatialite
```

### macOS (using Homebrew):
```bash
brew install gdal spatialite-tools
```

### Windows:
Download OSGeo4W: https://trac.osgeo.org/osgeo4w/
- Select "Express Install"
- Choose "GDAL" package

---

## 🚀 Launch in 2 Steps

### 1. Navigate to the project
```bash
cd geodjango_demo
```

### 2. Run the quick launch script
```bash
./quickstart.sh
```

That's it! The script will:
- ✅ Create a virtual environment (if needed)
- ✅ Install all dependencies
- ✅ Set up the SQLite database
- ✅ Create an admin user (username: `admin`, password: `admin`)
- ✅ Load 12 sample San Diego waypoints
- ✅ Start the development server

### 3. Open your browser
- **Home:** http://localhost:8000/
- **Map View:** http://localhost:8000/map/
- **Admin:** http://localhost:8000/admin/ (login: admin/admin)
- **API:** http://localhost:8000/api/waypoints/

---

## 🎯 Even Faster - Manual Commands

If you prefer to run commands manually:

```bash
# Create virtual environment (first time only)
python3 -m venv venv
source venv/bin/activate

# Install dependencies (first time only)
pip install -r requirements.txt

# Setup database (first time only)
python manage.py migrate
python manage.py createsuperuser  # Optional: create your own admin
python manage.py load_sample_data  # Load sample waypoints

# Start the server (every time)
python manage.py runserver
```

---

## 📱 What You'll See

### Home Page (/)
- List of 12 San Diego waypoints (parks, museums, landmarks, etc.)
- Category filter buttons (try clicking them - instant filtering with Alpine.js!)
- Clean, responsive design with Tailwind CSS

### Map View (/map/)
- Interactive Leaflet map centered on San Diego
- 12 markers for sample locations
- Click markers to see waypoint details
- Category filtering that updates markers in real-time

### Create Page (/create/)
- Form to add new waypoints
- Click on the map to select a location
- Fill in name, category, and description
- Submit to create (saves to SQLite database)

### Admin (/admin/)
- Login: `admin` / `admin`
- Full CRUD operations on waypoints
- Map widget for editing locations
- Search and filter capabilities

### API (/api/waypoints/)
- GeoJSON output for all waypoints
- Try these endpoints:
  - `/api/waypoints/` - All waypoints
  - `/api/waypoints/?category=park` - Only parks
  - `/api/waypoints/nearby/?lat=32.7157&lon=-117.1611&distance=10` - Nearby search

---

## 🔄 Key Changes from Original

**What Changed:**
- ✅ **Database:** SQLite + SpatiaLite (instead of PostgreSQL + PostGIS)
- ✅ **Setup:** No database server installation needed
- ✅ **Launch:** Single script execution
- ✅ **Dependencies:** Removed psycopg2 and GDAL requirements

**What Stayed the Same:**
- ✅ All GeoDjango features work
- ✅ Spatial queries work
- ✅ GeoJSON API works
- ✅ Maps work perfectly
- ✅ Admin interface works
- ✅ All three user interfaces work

**Note:** SQLite with SpatiaLite is perfect for demos and development. For production with large datasets, you'd want to use PostgreSQL + PostGIS (see the original README.md for those instructions).

---

## 🛑 Stopping the Server

Press `Ctrl+C` in the terminal where the server is running.

---

## 🔄 Restarting

After the initial setup, you only need:

```bash
cd geodjango_demo
source venv/bin/activate
python manage.py runserver
```

Or just run `./quickstart.sh` again - it will skip steps that are already done!

---

## 🎨 Try These Features

1. **Category Filtering** (Home page)
   - Click different category buttons
   - Watch the list filter instantly (no page reload!)

2. **Map Interaction** (Map view)
   - Click markers to see popup info
   - Try the category filter buttons
   - Watch markers update in real-time

3. **Create Waypoint** (Create page)
   - Click anywhere on the map
   - Fill in the form
   - Submit and see your new waypoint appear!

4. **API Exploration** (Browser or curl)
   ```bash
   curl http://localhost:8000/api/waypoints/ | json_pp
   ```

5. **Admin Management** (Admin)
   - Login with admin/admin
   - Edit waypoints
   - Use the map widget to change locations
   - Add new categories

---

## ⚠️ Troubleshooting

### "Command not found: ./quickstart.sh"
```bash
chmod +x quickstart.sh
./quickstart.sh
```

### "Python not found"
Make sure Python 3.10+ is installed:
```bash
python3 --version
```

### "Module not found"
Make sure you're in the virtual environment:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Port 8000 already in use
```bash
# Use a different port
python manage.py runserver 8001
```

### Database locked error (SQLite)
- This can happen if you stop the server abruptly
- Just restart it, or delete `db.sqlite3` and run migrations again

---

## 💡 Quick Tips

- **Sample data includes:** Balboa Park, USS Midway, Old Town, La Jolla Cove, Gaslamp Quarter, and more!
- **Admin is powerful:** Use it to quickly add/edit/delete waypoints
- **API is real:** The map view actually fetches data from `/api/waypoints/`
- **It's fully functional:** Despite using SQLite, all spatial queries work!

---

## 🎯 Next Steps

Once you've explored the demo:

1. **Review the code** - Check out `waypoints/models.py`, `views.py`, `serializers.py`
2. **Extend it** - Add new features, fields, or views
3. **Deploy it** - Follow the main README.md for production deployment
4. **Switch to PostgreSQL** - When ready for production, see the original setup instructions

---

## 📊 Demo Statistics

- **Launch time:** ~2 minutes (first time)
- **Subsequent launches:** ~5 seconds
- **Sample waypoints:** 12 San Diego locations
- **Database size:** ~100KB (SQLite file)
- **No external dependencies:** No PostgreSQL, no PostGIS server
- **Fully functional:** All GeoDjango features work!

---

**Enjoy exploring your GeoDjango demo!** 🗺️✨

Built with Django + GeoDjango + DRF + SQLite/SpatiaLite
