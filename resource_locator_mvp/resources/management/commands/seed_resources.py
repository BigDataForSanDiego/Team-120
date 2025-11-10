"""
Management command to seed the database with sample resources for testing.
"""
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from resources.models import Resource


class Command(BaseCommand):
    help = 'Seed database with sample resources for testing'

    def handle(self, *args, **kwargs):
        # Clear existing resources (optional)
        # Resource.objects.all().delete()
        
        sample_resources = [
            {
                'name': 'San Diego Food Bank',
                'rtype': 'food',
                'description': 'Free food distribution for families in need. Bring ID and proof of residence.',
                'address': '9850 Distribution Avenue, San Diego, CA 92121',
                'geom': Point(-117.1416, 32.9085, srid=4326),
                'phone': '(858) 576-1700',
                'website': 'https://sandiegofoodbank.org',
                'hours_json': {
                    'mon': [['09:00', '17:00']],
                    'tue': [['09:00', '17:00']],
                    'wed': [['09:00', '17:00']],
                    'thu': [['09:00', '17:00']],
                    'fri': [['09:00', '17:00']],
                },
                'state': 'visible',
            },
            {
                'name': 'Father Joe\'s Villages',
                'rtype': 'shelter',
                'description': 'Emergency shelter and supportive services for homeless individuals and families.',
                'address': '3350 E Street, San Diego, CA 92102',
                'geom': Point(-117.1294, 32.7074, srid=4326),
                'phone': '(619) 233-8197',
                'website': 'https://www.neighbor.org',
                'hours_json': {
                    'mon': [['00:00', '23:59']],
                    'tue': [['00:00', '23:59']],
                    'wed': [['00:00', '23:59']],
                    'thu': [['00:00', '23:59']],
                    'fri': [['00:00', '23:59']],
                    'sat': [['00:00', '23:59']],
                    'sun': [['00:00', '23:59']],
                },
                'state': 'visible',
            },
            {
                'name': 'Balboa Park Public Restrooms',
                'rtype': 'restroom',
                'description': 'Public restroom facilities available to all visitors.',
                'address': 'Balboa Park, San Diego, CA 92101',
                'geom': Point(-117.1469, 32.7341, srid=4326),
                'hours_json': {
                    'mon': [['06:00', '22:00']],
                    'tue': [['06:00', '22:00']],
                    'wed': [['06:00', '22:00']],
                    'thu': [['06:00', '22:00']],
                    'fri': [['06:00', '22:00']],
                    'sat': [['06:00', '22:00']],
                    'sun': [['06:00', '22:00']],
                },
                'state': 'visible',
            },
            {
                'name': 'Family Health Centers of San Diego',
                'rtype': 'medical',
                'description': 'Community health clinic providing medical, dental, and behavioral health services.',
                'address': '123 Euclid Avenue, San Diego, CA 92114',
                'geom': Point(-117.0910, 32.7088, srid=4326),
                'phone': '(619) 515-2300',
                'website': 'https://www.fhcsd.org',
                'hours_json': {
                    'mon': [['08:00', '17:00']],
                    'tue': [['08:00', '17:00']],
                    'wed': [['08:00', '17:00']],
                    'thu': [['08:00', '17:00']],
                    'fri': [['08:00', '17:00']],
                },
                'state': 'visible',
            },
            {
                'name': 'Legal Aid Society of San Diego',
                'rtype': 'legal',
                'description': 'Free legal services for low-income residents.',
                'address': '110 South Euclid Avenue, San Diego, CA 92114',
                'geom': Point(-117.0905, 32.7089, srid=4326),
                'phone': '(877) 534-2524',
                'website': 'https://www.lassd.org',
                'hours_json': {
                    'mon': [['08:30', '17:00']],
                    'tue': [['08:30', '17:00']],
                    'wed': [['08:30', '17:00']],
                    'thu': [['08:30', '17:00']],
                    'fri': [['08:30', '17:00']],
                },
                'state': 'visible',
            },
            {
                'name': 'Goodwill Donation Center - Downtown',
                'rtype': 'donation',
                'description': 'Drop off gently used clothing, household items, and more.',
                'address': '1935 National Avenue, San Diego, CA 92113',
                'geom': Point(-117.1359, 32.6889, srid=4326),
                'phone': '(619) 232-1948',
                'website': 'https://www.goodwillsandiego.org',
                'hours_json': {
                    'mon': [['09:00', '20:00']],
                    'tue': [['09:00', '20:00']],
                    'wed': [['09:00', '20:00']],
                    'thu': [['09:00', '20:00']],
                    'fri': [['09:00', '20:00']],
                    'sat': [['09:00', '20:00']],
                    'sun': [['10:00', '18:00']],
                },
                'state': 'visible',
            },
            {
                'name': 'St. Vincent de Paul Village',
                'rtype': 'shelter',
                'description': 'Comprehensive services including shelter, meals, and job training.',
                'address': '1501 Imperial Avenue, San Diego, CA 92101',
                'geom': Point(-117.1478, 32.7113, srid=4326),
                'phone': '(619) 233-8500',
                'website': 'https://www.svdpsd.org',
                'hours_json': {
                    'mon': [['00:00', '23:59']],
                    'tue': [['00:00', '23:59']],
                    'wed': [['00:00', '23:59']],
                    'thu': [['00:00', '23:59']],
                    'fri': [['00:00', '23:59']],
                    'sat': [['00:00', '23:59']],
                    'sun': [['00:00', '23:59']],
                },
                'state': 'visible',
            },
            {
                'name': 'Jacobs & Cushman San Diego Food Bank - North County',
                'rtype': 'food',
                'description': 'Food distribution and nutrition education programs.',
                'address': '1160 North Melrose Drive, Vista, CA 92083',
                'geom': Point(-117.2395, 33.2168, srid=4326),
                'phone': '(760) 940-1000',
                'website': 'https://sandiegofoodbank.org',
                'hours_json': {
                    'mon': [['09:00', '16:00']],
                    'wed': [['09:00', '16:00']],
                    'fri': [['09:00', '16:00']],
                },
                'state': 'visible',
            },
            {
                'name': 'Alpha Project for the Homeless',
                'rtype': 'shelter',
                'description': 'Emergency shelter and transitional housing programs.',
                'address': '3737 5th Avenue, San Diego, CA 92103',
                'geom': Point(-117.1600, 32.7491, srid=4326),
                'phone': '(619) 542-1877',
                'website': 'https://www.alphaproject.org',
                'hours_json': {
                    'mon': [['00:00', '23:59']],
                    'tue': [['00:00', '23:59']],
                    'wed': [['00:00', '23:59']],
                    'thu': [['00:00', '23:59']],
                    'fri': [['00:00', '23:59']],
                    'sat': [['00:00', '23:59']],
                    'sun': [['00:00', '23:59']],
                },
                'state': 'visible',
            },
            {
                'name': 'Feeding San Diego - Miramar Distribution Center',
                'rtype': 'food',
                'description': 'Food rescue and distribution serving San Diego County.',
                'address': '9850 Distribution Avenue, San Diego, CA 92121',
                'geom': Point(-117.1415, 32.9087, srid=4326),
                'phone': '(858) 863-4090',
                'website': 'https://feedingsandiego.org',
                'hours_json': {
                    'mon': [['08:00', '16:00']],
                    'tue': [['08:00', '16:00']],
                    'wed': [['08:00', '16:00']],
                    'thu': [['08:00', '16:00']],
                    'fri': [['08:00', '16:00']],
                },
                'state': 'visible',
            },
            {
                'name': 'Waterfront Park Public Restrooms',
                'rtype': 'restroom',
                'description': 'Clean public restrooms near the waterfront.',
                'address': '1600 Pacific Highway, San Diego, CA 92101',
                'geom': Point(-117.1709, 32.7207, srid=4326),
                'hours_json': {
                    'mon': [['06:00', '22:00']],
                    'tue': [['06:00', '22:00']],
                    'wed': [['06:00', '22:00']],
                    'thu': [['06:00', '22:00']],
                    'fri': [['06:00', '22:00']],
                    'sat': [['06:00', '22:00']],
                    'sun': [['06:00', '22:00']],
                },
                'state': 'visible',
            },
            {
                'name': 'Neighborhood Healthcare - Central',
                'rtype': 'medical',
                'description': 'Comprehensive healthcare services including primary care and dental.',
                'address': '1978 Corte Del Nogal, Carlsbad, CA 92011',
                'geom': Point(-117.2792, 33.1239, srid=4326),
                'phone': '(760) 736-6767',
                'website': 'https://www.nhcare.org',
                'hours_json': {
                    'mon': [['08:00', '17:00']],
                    'tue': [['08:00', '17:00']],
                    'wed': [['08:00', '17:00']],
                    'thu': [['08:00', '17:00']],
                    'fri': [['08:00', '17:00']],
                },
                'state': 'visible',
            },
            {
                'name': 'Casa Cornelia Law Center',
                'rtype': 'legal',
                'description': 'Free legal services for immigrants and refugees.',
                'address': '2060 India Street, San Diego, CA 92101',
                'geom': Point(-117.1692, 32.7304, srid=4326),
                'phone': '(619) 231-8414',
                'website': 'https://www.casacornelia.org',
                'hours_json': {
                    'mon': [['09:00', '17:00']],
                    'tue': [['09:00', '17:00']],
                    'wed': [['09:00', '17:00']],
                    'thu': [['09:00', '17:00']],
                    'fri': [['09:00', '17:00']],
                },
                'state': 'visible',
            },
            {
                'name': 'Salvation Army Donation Center',
                'rtype': 'donation',
                'description': 'Accept donations of clothing, furniture, and household goods.',
                'address': '4170 Pacific Highway, San Diego, CA 92110',
                'geom': Point(-117.2043, 32.7592, srid=4326),
                'phone': '(619) 297-3865',
                'website': 'https://www.salvationarmyusa.org',
                'hours_json': {
                    'mon': [['09:00', '18:00']],
                    'tue': [['09:00', '18:00']],
                    'wed': [['09:00', '18:00']],
                    'thu': [['09:00', '18:00']],
                    'fri': [['09:00', '18:00']],
                    'sat': [['09:00', '18:00']],
                    'sun': [['10:00', '17:00']],
                },
                'state': 'visible',
            },
            {
                'name': 'Rachel\'s Women\'s Center',
                'rtype': 'shelter',
                'description': 'Day center for homeless women providing showers, laundry, and meals.',
                'address': '1030 Seventh Avenue, San Diego, CA 92101',
                'geom': Point(-117.1590, 32.7174, srid=4326),
                'phone': '(619) 696-0640',
                'website': 'https://svdpsd.org/rachels',
                'hours_json': {
                    'mon': [['07:00', '15:00']],
                    'tue': [['07:00', '15:00']],
                    'wed': [['07:00', '15:00']],
                    'thu': [['07:00', '15:00']],
                    'fri': [['07:00', '15:00']],
                },
                'state': 'visible',
            },
        ]
        
        created_count = 0
        for resource_data in sample_resources:
            resource, created = Resource.objects.get_or_create(
                name=resource_data['name'],
                defaults=resource_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created: {resource.name}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\nSuccessfully created {created_count} sample resources!')
        )
