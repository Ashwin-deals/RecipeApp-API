"""if wait_for_db.py works correctly, this file mocks the needed parts. 
Tests custom Django management commands"""

from unittest.mock import patch
# This Lirary lets to mock the needed parts in the code 

from psycopg2 import OperationalError as Psycopg2Error
# Error when DB is not connected. 

from django.core.management import call_command
# Lets to run commands directly from the code instead of running through Terminal

from django.db.utils import OperationalError
# Operational Error is raised when django can't connect to the DB

from django.test import SimpleTestCase
# Helps to run unittest where DB is not needed 


@patch('core.management.commands.wait_for_db.Command.check')
# Locates check method from core.management..... and replaces with mock 
# Patch injects the mock into the first arguement in the function(patched_check)

class CommandTests(SimpleTestCase):
    def test_wait_for_db_ready(self, patched_check):
        patched_check.return_value = True
        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default']) # default is alias for the actual DB
        # Make sures Command.check is just checked once. 

    @patch('time.sleep') # Mocks sleep
    # When the DB fails it sleeps for a few seconds and tries again. 

    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]
        # 2 times - Faking that DB is not reachable 
        # 3 times - Still pretending that DB is not ready
        # 6th time DB is ready (True)

        
        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6) # Make sures command tried 6 times 
        patched_check.assert_called_with(databases=['default']) # Make sures the function was called in the correct database name