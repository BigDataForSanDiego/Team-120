"""
Sample data loader for GeoDjango demo.
Run this after migrations to populate the database with example waypoints.
"""
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from waypoints.models import Waypoint


class Command(BaseCommand):
    help = 'Load sample waypoint data for San Diego area'

    def handle(self, *args, **kwargs):
        # Clear existing data
        Waypoint.objects.all().delete()
        self.stdout.write('Cleared existing waypoints...')

        # Sample waypoints in San Diego area
        sample_waypoints = [
            {
                'name': 'Balboa Park',
                'category': 'park',
                'description': 'Urban cultural park with museums, gardens, and the San Diego Zoo',
                'location': Point(-117.1473, 32.7341, srid=4326)
            },
            {
                'name': 'USS Midway Museum',
                'category': 'museum',
                'description': 'Historic aircraft carrier museum on the waterfront',
                'location': Point(-117.1751, 32.7137, srid=4326)
            },
            {
                'name': 'Old Town San Diego State Historic Park',
                'category': 'landmark',
                'description': 'Historic park celebrating the Mexican and early American periods of San Diego history',
                'location': Point(-117.1945, 32.7549, srid=4326)
            },
            {
                'name': 'Cabrillo National Monument',
                'category': 'landmark',
                'description': 'National monument commemorating the landing of Juan Rodríguez Cabrillo',
                'location': Point(-117.2419, 32.6734, srid=4326)
            },
            {
                'name': 'La Jolla Cove',
                'category': 'park',
                'description': 'Scenic cove with sea lions and snorkeling opportunities',
                'location': Point(-117.2713, 32.8509, srid=4326)
            },
            {
                'name': 'Gaslamp Quarter',
                'category': 'landmark',
                'description': 'Historic heart of San Diego with Victorian-era buildings',
                'location': Point(-117.1605, 32.7142, srid=4326)
            },
            {
                'name': 'San Diego Zoo',
                'category': 'other',
                'description': 'World-famous zoo in Balboa Park',
                'location': Point(-117.1511, 32.7353, srid=4326)
            },
            {
                'name': 'Coronado Beach',
                'category': 'park',
                'description': 'Wide, sandy beach with iconic Hotel del Coronado',
                'location': Point(-117.1825, 32.6859, srid=4326)
            },
            {
                'name': 'Seaport Village',
                'category': 'other',
                'description': 'Waterfront shopping and dining complex',
                'location': Point(-117.1704, 32.7092, srid=4326)
            },
            {
                'name': 'Santa Fe Depot',
                'category': 'transit',
                'description': 'Historic train station serving Amtrak and Coaster',
                'location': Point(-117.1697, 32.7160, srid=4326)
            },
            {
                'name': 'The Fish Market',
                'category': 'restaurant',
                'description': 'Waterfront seafood restaurant with harbor views',
                'location': Point(-117.1697, 32.7119, srid=4326)
            },
            {
                'name': 'Mission Bay Park',
                'category': 'park',
                'description': 'Large aquatic park with beaches and recreation areas',
                'location': Point(-117.2261, 32.7637, srid=4326)
            },
        ]

        # Create waypoints
        for data in sample_waypoints:
            waypoint = Waypoint.objects.create(**data)
            self.stdout.write(self.style.SUCCESS(f'Created waypoint: {waypoint.name}'))

        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully loaded {len(sample_waypoints)} sample waypoints!'))
        self.stdout.write('Visit http://localhost:8000/ to see them.')
