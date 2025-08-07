"""If wait_for_db.py works correctly, this file mocks the needed parts."""

from unittest.mock import patch
# This library lets us mock the needed parts in the code

from psycopg2 import OperationalError as Psycopg2Error
# Error when DB is not connected

from django.core.management import call_command
# Lets us run commands directly from code instead of using Terminal

from django.db.utils import OperationalError
# Raised when Django can't connect to the DB

from django.test import SimpleTestCase
# Helps run unittests where DB is not needed


@patch('core.management.commands.wait_for_db.Command.check')
# Locates check method and replaces with mock
# Patch injects the mock into the first argument (patched_check)
class CommandTests(SimpleTestCase):

    def test_wait_for_db_ready(self, patched_check):
        patched_check.return_value = True
        call_command('wait_for_db')

        patched_check.assert_called_once_with(
            databases=['default']
        )
        # Ensures Command.check is just checked once

    @patch('time.sleep')  # Mocks sleep
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        patched_check.side_effect = (
            [Psycopg2Error] * 2 +
            [OperationalError] * 3 +
            [True]
        )
        # 2 times: faking DB unreachable
        # 3 times: DB still not ready
        # 6th time: DB is ready

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        # Ensures command tried 6 times

        patched_check.assert_called_with(databases=['default'])
        # Ensures DB alias is correct
