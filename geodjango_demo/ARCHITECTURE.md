# 🗺️ GeoDjango Demo - Architecture Overview

## Project Purpose
This demo application showcases a complete implementation of the **Django + GeoDjango + DRF** stack as outlined in your Notion page. It serves as a reference implementation for building geospatial web applications.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend Layer                        │
├─────────────────────────────────────────────────────────────┤
│  • Django Templates (Server-Side Rendering)                  │
│  • HTMX (Progressive Enhancement)                            │
│  • Alpine.js (Reactive Components)                           │
│  • Leaflet.js (Interactive Maps)                             │
│  • Tailwind CSS (Styling)                                    │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│                      Application Layer                       │
├─────────────────────────────────────────────────────────────┤
│  Django 5.x                                                  │
│  ├── GeoDjango (Spatial Database ORM)                        │
│  ├── Django REST Framework (API Layer)                       │
│  ├── DRF-GIS (GeoJSON Serialization)                         │
│  └── Django Admin (Management Interface)                     │
└──────────────────┬──────────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────────┐
│                       Database Layer                         │
├─────────────────────────────────────────────────────────────┤
│  PostgreSQL 14+                                              │
│  └── PostGIS Extension                                       │
│      ├── Geometry/Geography Types                            │
│      ├── Spatial Indexes (GIST)                              │
│      └── Spatial Functions (ST_DWithin, ST_Distance, etc.)   │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. User Creates Waypoint
```
User clicks map → Leaflet captures lat/lon → Alpine.js updates form state
→ Form POST to Django → Django creates Waypoint with PostGIS Point
→ Saves to PostgreSQL → Redirects to list view
```

### 2. API Request (GeoJSON)
```
Client requests /api/waypoints/ → DRF ViewSet queries database
→ GeoFeatureModelSerializer converts to GeoJSON → Returns FeatureCollection
→ Leaflet renders markers on map
```

### 3. Spatial Query (Nearby)
```
Client requests /api/waypoints/nearby/?lat=X&lon=Y&distance=5
→ PostGIS ST_DWithin query → Returns waypoints within radius
→ Serialized as GeoJSON → Rendered on map
```

## Key Components

### Models (`waypoints/models.py`)
```python
class Waypoint(models.Model):
    location = models.PointField(geography=True)  # PostGIS point
    # ... other fields
```
- Uses `PointField` with `geography=True` for accurate distance calculations
- Supports spatial indexing and queries

### Serializers (`waypoints/serializers.py`)
```python
class WaypointSerializer(GeoFeatureModelSerializer):
    geo_field = "location"  # Outputs GeoJSON
```
- `GeoFeatureModelSerializer` automatically converts to GeoJSON format
- Compatible with Leaflet and other mapping libraries

### Views (`waypoints/views.py`)
- **ViewSets:** REST API endpoints with DRF
- **Template Views:** Server-side rendered pages
- **Custom Actions:** `nearby()` for distance-based queries

### Templates
1. **base.html:** Layout with navigation
2. **waypoint_list.html:** Home page with filtering
3. **waypoint_create.html:** Form with map picker
4. **waypoint_map.html:** Full interactive map

### Admin (`waypoints/admin.py`)
- Extends `GISModelAdmin` for map widgets
- Click-to-edit location on a map
- Search, filter, and bulk operations

## API Endpoints

| Endpoint | Method | Description | Response Format |
|----------|--------|-------------|-----------------|
| `/api/waypoints/` | GET | List all waypoints | GeoJSON FeatureCollection |
| `/api/waypoints/?category=park` | GET | Filter by category | GeoJSON FeatureCollection |
| `/api/waypoints/nearby/` | GET | Find nearby waypoints | GeoJSON FeatureCollection |
| `/api/waypoints/{id}/` | GET | Get single waypoint | GeoJSON Feature |

## Frontend Strategy (Thin Client)

Following the Notion guidelines, this demo uses a **thin client** approach:

### Traditional JavaScript SPA ❌
- Heavy client-side frameworks (React, Vue)
- Large bundle sizes
- Complex state management
- SEO challenges

### This Demo's Approach ✅
- **Server-side rendering** for initial page load
- **HTMX** for dynamic updates without full page reloads
- **Alpine.js** for minimal reactive UI (filtering, form state)
- **Leaflet** only where maps are needed
- **Total JS payload:** ~50KB (vs. 500KB+ for SPAs)

### Benefits
- Fast initial load
- Works on low-power devices
- SEO-friendly
- Progressive enhancement

## Database Schema

### Waypoint Table
```sql
CREATE TABLE waypoints_waypoint (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    category VARCHAR(100),
    description TEXT,
    location GEOGRAPHY(Point, 4326),  -- PostGIS type
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE INDEX idx_waypoint_location ON waypoints_waypoint USING GIST(location);
```

### Spatial Queries
```python
# Find waypoints within 5km of a point
Waypoint.objects.filter(
    location__distance_lte=(point, D(km=5))
)

# Order by distance
Waypoint.objects.distance(point).order_by('distance')
```

## Security Features

1. **CSRF Protection:** Django's built-in CSRF tokens on all forms
2. **SQL Injection:** Parameterized queries via Django ORM
3. **XSS Protection:** Template auto-escaping
4. **Authentication:** Django auth system (extendable with django-allauth)
5. **CORS:** Configurable with django-cors-headers

## Performance Optimizations

1. **Spatial Indexes:** GIST indexes on `location` field
2. **Database Indexes:** On category and created_at
3. **Query Optimization:** `select_related()` and `prefetch_related()`
4. **Pagination:** API returns 50 results per page
5. **Static Files:** Served via CDN in production

## Deployment Checklist

- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Generate strong `SECRET_KEY`
- [ ] Set up managed PostgreSQL with PostGIS
- [ ] Configure static file serving (Nginx or CDN)
- [ ] Set up SSL/TLS certificates
- [ ] Configure CORS headers for API
- [ ] Set up monitoring and logging
- [ ] Run `collectstatic` for production
- [ ] Use Gunicorn with multiple workers

## Extension Ideas

This demo can be extended with:

1. **User Authentication:** Add user accounts and permissions
2. **Categories Management:** Allow admins to create custom categories
3. **Photo Uploads:** Add image fields for waypoints
4. **Reviews/Ratings:** Let users rate waypoints
5. **Search:** Full-text search with PostgreSQL
6. **Clustering:** Marker clustering for dense areas
7. **Routes:** Connect waypoints to create routes/paths
8. **Analytics:** Track popular waypoints and user behavior

## Stack Comparison

| Feature | This Demo | Typical SPA |
|---------|-----------|-------------|
| Initial Load | < 1s | 2-5s |
| JS Bundle Size | ~50KB | 500KB+ |
| Server CPU | Low | Low |
| Client CPU | Very Low | Medium-High |
| SEO | Native | Requires SSR |
| Complexity | Medium | High |
| Mobile Performance | Excellent | Good |

## Files Overview

```
geodjango_demo/
├── manage.py                      # Django CLI
├── requirements.txt               # Python dependencies
├── .env.example                   # Environment template
├── setup.sh                       # Automated setup script
├── README.md                      # Full documentation
├── QUICKSTART.md                  # Quick start guide
├── ARCHITECTURE.md                # This file
│
├── geodjango_demo/                # Project config
│   ├── settings.py                # Django + GeoDjango settings
│   ├── urls.py                    # URL routing
│   ├── wsgi.py                    # WSGI server config
│   └── asgi.py                    # ASGI server config
│
├── waypoints/                     # Main app
│   ├── models.py                  # Waypoint model (PointField)
│   ├── serializers.py             # DRF serializers (GeoJSON)
│   ├── views.py                   # API + template views
│   ├── forms.py                   # Django forms
│   ├── admin.py                   # Admin with GIS widgets
│   └── management/commands/
│       └── load_sample_data.py    # Sample data loader
│
└── templates/                     # Django templates
    ├── base.html                  # Base layout
    └── waypoints/
        ├── waypoint_list.html     # Home page
        ├── waypoint_create.html   # Create form
        └── waypoint_map.html      # Map view
```

## Learning Resources

- **GeoDjango Tutorial:** https://docs.djangoproject.com/en/stable/ref/contrib/gis/tutorial/
- **PostGIS Functions:** https://postgis.net/docs/reference.html
- **DRF Tutorial:** https://www.django-rest-framework.org/tutorial/quickstart/
- **Leaflet Docs:** https://leafletjs.com/reference.html
- **HTMX Examples:** https://htmx.org/examples/

---

**Built for:** BDA Hackathon 2025  
**Tech Stack:** Django 5.x + GeoDjango + DRF + PostGIS + Leaflet  
**Architecture:** Thin Client with Progressive Enhancement
