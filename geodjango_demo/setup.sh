#!/bin/bash

# GeoDjango Demo Setup Script
# This script automates the initial setup process

echo "🚀 GeoDjango Demo Setup"
echo "======================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.10 or higher."
    exit 1
fi

echo "✓ Python 3 found"

# Check if PostgreSQL is available
if ! command -v psql &> /dev/null; then
    echo "⚠️  PostgreSQL not found. Please install PostgreSQL with PostGIS extension."
    echo "   Ubuntu/Debian: sudo apt-get install postgresql postgis"
    echo "   macOS: brew install postgresql postgis"
    exit 1
fi

echo "✓ PostgreSQL found"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "⚙️  Creating .env file..."
    cp .env.example .env
    echo "✓ Created .env file (please update with your database credentials)"
else
    echo "✓ .env file already exists"
fi

# Run migrations
echo ""
echo "🗄️  Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser
echo ""
echo "👤 Create a superuser account for admin access"
python manage.py createsuperuser

# Load sample data
echo ""
echo "📍 Loading sample waypoint data..."
python manage.py load_sample_data

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎉 Next steps:"
echo "   1. Ensure PostgreSQL is running with PostGIS extension enabled"
echo "   2. Update .env with your database credentials if needed"
echo "   3. Run: python manage.py runserver"
echo "   4. Visit: http://localhost:8000/"
echo ""
echo "📚 Useful URLs:"
echo "   - Home: http://localhost:8000/"
echo "   - Admin: http://localhost:8000/admin/"
echo "   - API: http://localhost:8000/api/waypoints/"
echo "   - Map: http://localhost:8000/map/"
echo ""
