"""Empty migration placeholder.

This file was previously a misplaced view (nominatim_proxy). The actual view
is defined in `resources/views_proxy.py`. Django treats any .py file in the
`migrations` package as a migration file, so this file caused a
BadMigrationError because it lacked a Migration class.

Keep a minimal Migration class here so Django's migration loader is happy and
we preserve the existing migration ordering. If you prefer to remove this
placeholder, delete this file and ensure migrations are re-generated.
"""

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("resources", "0001_initial"),
    ]

    operations = []

