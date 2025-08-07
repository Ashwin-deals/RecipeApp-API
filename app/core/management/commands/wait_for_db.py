"""
Real Django command to wait for Database to be available 
"""
import time
from psycopg2 import OperationalError as Psycopg20pError
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand

# * - gets input in a Tuple. ** - Dictionary
class Command(BaseCommand):
    def handle(self, *args, **optional): # Positional arguements, Keyword arguements. Must include them.
        self.stdout.write('Waiting for database...')
        db_up = False # Initially the database should be not connected 
        while db_up is False:
            try:  # Tries to check the DB connection
                self.check(databases=['default'])
                db_up = True
            except(Psycopg20pError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1) # Waits for a second before trying again

        self.stdout.write(self.style.SUCCESS('Databases available!')) # Green text