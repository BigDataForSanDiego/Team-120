"""
ASGI config for geodjango_demo project.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'geodjango_demo.settings')

application = get_asgi_application()
