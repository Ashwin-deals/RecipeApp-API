"""
Real Django command to wait for Database to be available
"""
import time

from psycopg2 import OperationalError as Psycopg2OpError
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


# *args - Positional arguments (as tuple),
# **kwargs - Keyword arguments (as dict)
class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        self.stdout.write('Waiting for database...')
        db_up = False  # Initially, assume database is not connected

        while db_up is False:
            try:
                # Try checking DB connection
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write(
                    'Database unavailable, waiting 1 second...'
                )
                time.sleep(1)  # Wait 1 second before trying again

        # Print in green if DB is ready
        self.stdout.write(
            self.style.SUCCESS('Database available!')
        )
