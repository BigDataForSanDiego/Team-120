# Big Data Hackathon for San Diego 2025 - Team 120

## 🗺️ GeoDjango Demo Application

A complete demonstration of **Django + GeoDjango + DRF** for building geospatial web applications, created as a reference implementation for the team.

### ⚡ INSTANT LAUNCH - No Database Setup Required!

**New:** Run the demo immediately with SQLite (no PostgreSQL needed):

```bash
cd geodjango_demo
./quickstart.sh
```

Then visit: **http://localhost:8000/**

See **[LAUNCH.md](geodjango_demo/LAUNCH.md)** for the 2-minute quick start!

---

### 📁 Project Location
The demo application is located in the **`geodjango_demo/`** directory.

### 🚀 Quick Start Options

**Option 1: Instant Demo (SQLite)**
```bash
cd geodjango_demo
./quickstart.sh  # Automated setup with SQLite - no database server needed!
```

**Option 2: Production Setup (PostgreSQL)**
```bash
cd geodjango_demo
# Follow README.md for PostgreSQL + PostGIS setup
```

### 📚 Documentation
- **[README.md](geodjango_demo/README.md)** - Complete setup guide with all details
- **[QUICKSTART.md](geodjango_demo/QUICKSTART.md)** - 5-minute quick start for team members
- **[ARCHITECTURE.md](geodjango_demo/ARCHITECTURE.md)** - Architecture deep-dive and data flow

### 🎯 What This Demo Shows
- ✅ GeoDjango integration with PostGIS
- ✅ RESTful GeoJSON API with Django REST Framework
- ✅ Interactive Leaflet maps for visualization
- ✅ Admin interface with geospatial widgets
- ✅ Thin client UI using HTMX + Alpine.js
- ✅ Sample San Diego waypoint data (12 locations)

### 🧱 Tech Stack
Based on the **[Notion Stack Overview](https://www.notion.so/2a5eb3065110802789f7dc41a51f62ff)**:
- Django 5.x + GeoDjango
- Django REST Framework + DRF-GIS
- PostgreSQL + PostGIS
- Leaflet for interactive maps
- HTMX + Alpine.js for minimal JavaScript
- Tailwind CSS for styling

### 📸 What's Included
1. **Waypoint Model** - GeoDjango PointField with categories
2. **GeoJSON API** - RESTful endpoints with spatial queries (nearby search)
3. **Three User Interfaces:**
   - List view with category filtering
   - Create form with interactive map picker
   - Full map visualization
4. **Django Admin** - Built-in admin with GIS widgets for data management
5. **Sample Data** - 12 San Diego landmarks and locations preloaded

### 🔗 URLs (after running server)
- **Home:** http://localhost:8000/
- **Admin:** http://localhost:8000/admin/
- **API:** http://localhost:8000/api/waypoints/
- **Map View:** http://localhost:8000/map/

---

## Hackathon Proposal Guidelines

<!-- ~~## NOV 8 (Day 1): Proposal Submission Guidelines~~ -->
## NOV 8 (Day 1): Proposal Submission Guidelines
> - Get a markdown template, [proposal_submission_form_2025.md](https://github.com/BigDataForSanDiego/bigdataforsandiego.github.io/blob/master/templates/proposal_submission_form_2025.md), which should be available in your GitHub team repository
> - Customize the template and rename it as README.md to replace the original README.md file **by 4:30 p.m.**

> - For a proposal, please provide us with the following:
>   - Your team name and members
>   - A title for your idea
>   - Hackathon theme it ties to (see list on site)
>   - A sentence describing your idea
>   - A visual that shows what your idea is (can be a sketch, photo, wireframe, etc.)
> - Make sure to think about the Hackathon theme, how this will help the user experience, how data will be incorporated and what problem it aims to solve. 

