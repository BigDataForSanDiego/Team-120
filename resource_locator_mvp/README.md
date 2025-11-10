# Resource Locator MVP

A Django + GeoDjango web application for locating resources (food banks, shelters, medical services, etc.) for people experiencing homelessness in San Diego County.

**BDA Hackathon 2025 Project**

## Features

### MVP (v0.1) Functionality

- **Anonymous User Access**: 
  - Interactive map with resource markers
  - Filter by resource type (food, shelter, restroom, medical, legal, donation)
  - Distance-based filtering (1-10 miles)
  - "Open now" filter based on hours of operation
  - Detailed resource information cards
  - No login required for browsing

- **Service Provider Portal**:
  - Authenticated submission of new resources
  - Edit own resources (if visible or not_visible)
  - Map-based location picker
  - Resource expiration dates
  - View submission status

- **Admin Moderation**:
  - Full CRUD operations on all resources
  - Approve/hide/reject resource submissions
  - GeoDjango admin with map widgets
  - Filter by state and resource type
  - Add rejection reasons

## Tech Stack

- **Backend**: Django 5.0.9 + GeoDjango
- **Database**: PostgreSQL + PostGIS
- **API**: Django REST Framework + django-rest-framework-gis
- **Frontend**: 
  - Leaflet.js (map rendering)
  - Alpine.js (lightweight reactivity)
  - HTMX (dynamic updates)
  - Vanilla CSS (no framework)
- **Deployment**: Gunicorn (production server)

## Prerequisites

- Python 3.10+
- PostgreSQL 14+ with PostGIS extension
- GDAL/GEOS libraries (for GeoDjango)

### Installing GDAL/GEOS (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install -y binutils libproj-dev gdal-bin postgresql-14-postgis-3
```

### Installing GDAL/GEOS (macOS)

```bash
brew install postgresql postgis gdal
```

## Project Setup

### 1. Clone and Create Virtual Environment

```bash
cd resource_locator_mvp
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Database Setup

Create a PostgreSQL database with PostGIS:

```bash
sudo -u postgres psql
```

In PostgreSQL shell:

```sql
CREATE DATABASE resource_locator_db;
\c resource_locator_db
CREATE EXTENSION postgis;
\q
```

### 4. Environment Configuration

Copy the example environment file and update with your settings:

```bash
cp .env.example .env
```

Edit `.env` and set:

```
DB_NAME=resource_locator_db
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432

SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Admin User

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 7. Load Sample Data

```bash
python manage.py seed_resources
```

This will create 15 sample resources across San Diego County.

### 8. Run Development Server

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000 to see the application.

## Usage

### Anonymous Users (Homepage)

1. Visit http://127.0.0.1:8000
2. Click "Use My Location" or enter an address
3. Use filter chips to select resource types
4. Adjust distance radius
5. Toggle "Show only open now" to see currently open resources
6. Click markers on map or cards in list to view details

### Service Providers

1. Login at http://127.0.0.1:8000/accounts/login/
2. Access dashboard at http://127.0.0.1:8000/provider/
3. Click "Add New Resource"
4. Fill out form and click map to set location
5. Submit for review

### Administrators

1. Login to admin at http://127.0.0.1:8000/admin/
2. Navigate to Resources section
3. Filter by state (visible/not_visible/rejected)
4. Edit resources using map widget
5. Moderate submissions by changing state
6. Add rejection reasons when rejecting

## API Endpoints

### Public API (No Auth Required)

- `GET /api/resources/` - List all visible resources (GeoJSON format)
  - Query params:
    - `rtype`: Filter by type (e.g., `food,shelter`)
    - `lat`, `lon`: User location
    - `radius_m`: Search radius in meters
    - `open_now`: Filter to open resources (`true`)

- `GET /api/resources/{id}/` - Get single resource

### Provider API (Auth Required)

- `GET /api/provider/resources/` - List provider's resources
- `POST /api/provider/resources/` - Create new resource
- `GET /api/provider/resources/{id}/` - Get resource detail
- `PUT/PATCH /api/provider/resources/{id}/` - Update resource
- `DELETE /api/provider/resources/{id}/` - Delete resource

### Admin API (Admin Auth Required)

- `GET /api/admin/resources/` - List all resources
  - Query param `state`: Filter by state
- `POST /api/admin/resources/` - Create resource
- `GET /api/admin/resources/{id}/` - Get resource detail
- `PUT/PATCH /api/admin/resources/{id}/` - Update resource
- `DELETE /api/admin/resources/{id}/` - Delete resource
- `PATCH /api/admin/resources/{id}/moderate/` - Moderate resource
  - Body: `{"state": "visible|not_visible|rejected", "rejection_reason": "..."}`

## Data Model

### Resource Model

- **name**: Resource name (required)
- **rtype**: Resource type - food, shelter, restroom, medical, legal, donation, other
- **description**: Detailed description
- **hours_json**: Weekly hours in JSON format
- **phone**: Contact phone
- **email**: Contact email
- **website**: Website URL
- **address**: Street address
- **geom**: Geographic point (PostGIS PointField)
- **tags**: JSON array of tags
- **state**: Moderation state - visible, not_visible, rejected
- **rejection_reason**: Admin-provided rejection reason
- **provider**: Foreign key to User (who submitted)
- **expires_at**: Optional expiration date
- **created_at**: Creation timestamp
- **updated_at**: Last update timestamp

### Hours JSON Format

```json
{
  "mon": [["09:00", "17:00"]],
  "tue": [["09:00", "17:00"]],
  "wed": [["09:00", "17:00"]],
  "thu": [["09:00", "17:00"]],
  "fri": [["09:00", "17:00"]],
  "sat": [["10:00", "16:00"]],
  "sun": []
}
```

Multiple time ranges per day are supported:
```json
{
  "mon": [["09:00", "12:00"], ["13:00", "17:00"]]
}
```

## Project Structure

```
resource_locator_mvp/
├── config/                     # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── resources/                  # Main Django app
│   ├── management/
│   │   └── commands/
│   │       └── seed_resources.py
│   ├── migrations/
│   ├── admin.py               # Django admin configuration
│   ├── forms.py               # Provider submission forms
│   ├── models.py              # Resource model
│   ├── provider_views.py      # Provider dashboard views
│   ├── serializers.py         # DRF serializers
│   ├── urls.py                # URL routing
│   └── views.py               # API viewsets
├── templates/
│   ├── base.html
│   ├── home.html              # Anonymous user map page
│   ├── provider/
│   │   ├── dashboard.html
│   │   ├── resource_form.html
│   │   └── resource_confirm_delete.html
│   └── registration/
│       └── login.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── map.js             # Leaflet map logic
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Development Notes

### Open Now Logic

The `is_open_now()` method on the Resource model checks if the current time falls within any of the resource's operating hours for the current day of the week. It handles:
- Multiple time ranges per day
- Overnight hours (e.g., 23:00 to 02:00)
- Timezone awareness (configured for America/Los_Angeles)

### Distance Filtering

Distance calculations use PostGIS's `ST_DWithin` for efficient spatial queries. Results are ordered by distance using `ST_Distance`.

### Map Icons

Resource markers are color-coded by type:
- Food: Green
- Shelter: Red
- Restroom: Blue
- Medical: Purple
- Legal: Orange
- Donation: Teal
- Other: Gray

### Thin Client Design

The application follows a thin client architecture:
- Server-side rendering with Django templates
- Minimal JavaScript (Alpine.js for reactivity, Leaflet for maps)
- Progressive enhancement approach
- Works on low-power mobile devices

## Deployment Considerations

### Production Checklist

1. Set `DEBUG=False` in `.env`
2. Configure `ALLOWED_HOSTS` with your domain
3. Generate new `SECRET_KEY`
4. Use managed PostgreSQL with PostGIS (e.g., Supabase, Neon, AWS RDS)
5. Serve static files via Nginx or CDN
6. Use Gunicorn for WSGI server
7. Set up HTTPS with SSL certificate
8. Configure logging and monitoring

### Environment Variables for Production

```
DB_NAME=production_db
DB_USER=production_user
DB_PASSWORD=strong_password
DB_HOST=your-postgres-host.com
DB_PORT=5432

SECRET_KEY=long-random-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### Running with Gunicorn

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```

## Future Enhancements (Out of MVP Scope)

- Multi-language support (Spanish translation)
- Real-time bed availability for shelters
- User accounts for anonymous users (save favorites)
- Polygon-based service areas (not just points)
- Mobile app (PWA or native)
- Email notifications for providers
- Bulk data import from CSV/APIs
- Analytics dashboard
- SMS integration for resource lookup

## License

This project is created for the BDA Hackathon 2025.

## Contact

For questions about this project, please contact the development team.
