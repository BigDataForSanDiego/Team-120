# Quick Start Guide

## Prerequisites Check

Before starting, ensure you have:
- [ ] Python 3.10 or higher
- [ ] PostgreSQL 14 or higher
- [ ] GDAL/GEOS libraries installed

## Installation Steps

### 1. Database Setup (5 minutes)

```bash
# Start PostgreSQL service
sudo service postgresql start

# Create database
sudo -u postgres psql << EOF
CREATE DATABASE resource_locator_db;
\c resource_locator_db
CREATE EXTENSION postgis;
\q
EOF
```

### 2. Python Environment (2 minutes)

```bash
cd /home/robert/Team-120/resource_locator_mvp

# Activate virtual environment (already created)
source venv/bin/activate

# Verify dependencies are installed
pip list | grep Django
```

### 3. Configure Environment (1 minute)

```bash
# Copy environment template
cp .env.example .env

# Edit .env if needed (optional - defaults should work)
nano .env
```

### 4. Initialize Database (3 minutes)

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: [choose a password]
```

### 5. Load Sample Data (1 minute)

```bash
python manage.py seed_resources
```

You should see:
```
Created: San Diego Food Bank
Created: Father Joe's Villages
...
Successfully created 15 sample resources!
```

### 6. Start Server (1 minute)

```bash
python manage.py runserver
```

## Access the Application

### Anonymous User (Homepage)
**URL**: http://127.0.0.1:8000

**Try this**:
1. Click "Use My Location" button
2. Select "Food" and "Shelter" filter chips
3. Toggle "Show only open now"
4. Click on a green or red marker
5. View resource details in modal

### Provider Dashboard
**URL**: http://127.0.0.1:8000/accounts/login/

**Try this**:
1. First, create a provider account via admin:
   - Go to http://127.0.0.1:8000/admin/
   - Login with superuser credentials
   - Go to Users → Add user
   - Create: username: `provider1`, password: `testpass123`
   
2. Login at http://127.0.0.1:8000/accounts/login/
   - Username: `provider1`
   - Password: `testpass123`

3. Click "Add New Resource"
4. Fill form and click map to set location
5. Submit resource

### Admin Interface
**URL**: http://127.0.0.1:8000/admin/

**Try this**:
1. Login with superuser credentials
2. Navigate to Resources → Resources
3. Click on any resource
4. Edit using map widget
5. Try changing State to "not_visible"

## API Testing

### Test Public API (No Auth)

```bash
# Get all visible resources
curl "http://127.0.0.1:8000/api/resources/"

# Filter by type
curl "http://127.0.0.1:8000/api/resources/?rtype=food,shelter"

# Filter by location and radius (3 miles around downtown SD)
curl "http://127.0.0.1:8000/api/resources/?lat=32.7157&lon=-117.1611&radius_m=4828"

# Get only open resources
curl "http://127.0.0.1:8000/api/resources/?open_now=true"
```

### Test Provider API (Auth Required)

First, get an auth token or use Django session auth:

```bash
# Login to get session cookie
curl -c cookies.txt -d "username=provider1&password=testpass123" \
  http://127.0.0.1:8000/accounts/login/

# List provider's resources
curl -b cookies.txt "http://127.0.0.1:8000/api/provider/resources/"
```

## Troubleshooting

### Issue: ModuleNotFoundError: No module named 'django.contrib.gis'

**Solution**: Install GDAL/GEOS libraries

```bash
# Ubuntu/Debian
sudo apt-get install binutils libproj-dev gdal-bin

# macOS
brew install gdal
```

### Issue: FATAL: database "resource_locator_db" does not exist

**Solution**: Create the database

```bash
sudo -u postgres psql -c "CREATE DATABASE resource_locator_db;"
```

### Issue: ERROR: could not load library: PostGIS

**Solution**: Install PostGIS extension

```bash
# Ubuntu/Debian
sudo apt-get install postgresql-14-postgis-3

# Then enable in database
sudo -u postgres psql resource_locator_db -c "CREATE EXTENSION postgis;"
```

### Issue: No resources showing on map

**Solutions**:
1. Make sure seed data loaded: `python manage.py seed_resources`
2. Check resources are visible: Go to admin and verify State = "visible"
3. Check browser console for JavaScript errors
4. Verify API returns data: Visit http://127.0.0.1:8000/api/resources/

## Common Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Start server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Load sample data
python manage.py seed_resources

# Create superuser
python manage.py createsuperuser

# Shell (for debugging)
python manage.py shell

# Collect static files (for production)
python manage.py collectstatic
```

## Next Steps

1. **Customize Sample Data**: Edit `resources/management/commands/seed_resources.py`
2. **Add More Resource Types**: Edit `TYPE_CHOICES` in `resources/models.py`
3. **Customize Map Center**: Edit default lat/lon in templates and settings
4. **Add Email Notifications**: Install django-mailer and configure SMTP
5. **Deploy to Production**: See README.md for deployment checklist

## Getting Help

- Check `README.md` for detailed documentation
- Check `SCAFFOLDING_SUMMARY.md` for implementation details
- Review Django admin for data management
- Check browser console for JavaScript errors
- Check terminal for Python errors

## Success Indicators

You'll know everything is working when:
- ✅ Homepage loads with a map centered on San Diego
- ✅ 15 markers appear on the map (various colors)
- ✅ Clicking "Food" filter shows only green markers
- ✅ Provider login redirects to dashboard
- ✅ Admin interface shows resources with map preview
- ✅ API returns GeoJSON at http://127.0.0.1:8000/api/resources/

Enjoy your Resource Locator MVP! 🎉
