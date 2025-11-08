#!/bin/bash

# Quick Launch Script for GeoDjango Demo
# Uses SQLite with SpatiaLite - no PostgreSQL setup needed!

echo "🚀 GeoDjango Demo - Quick Launch"
echo "================================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.10 or higher."
    exit 1
fi

echo "✓ Python 3 found"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo ""
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "📦 Installing dependencies (this may take a minute)..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Run migrations
echo ""
echo "🗄️  Setting up database..."
python manage.py makemigrations waypoints --noinput
python manage.py migrate --noinput

# Create superuser automatically (non-interactive)
echo ""
echo "👤 Creating admin user (username: admin, password: admin)..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print('✓ Admin user created')
else:
    print('✓ Admin user already exists')
EOF

# Load sample data
echo ""
echo "📍 Loading sample waypoint data..."
python manage.py load_sample_data

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎉 Starting development server..."
echo ""
echo "📚 Access the application at:"
echo "   • Home:  http://localhost:8000/"
echo "   • Admin: http://localhost:8000/admin/"
echo "   • API:   http://localhost:8000/api/waypoints/"
echo "   • Map:   http://localhost:8000/map/"
echo ""
echo "🔐 Admin credentials:"
echo "   Username: admin"
echo "   Password: admin"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
python manage.py runserver
