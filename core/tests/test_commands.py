from django.core.management import call_command
from django.test import TestCase
from core.models import Items


class GenerateDataCommandTest(TestCase):
    def test_generate_data_creates_items(self):
        self.assertEqual(Items.objects.count(), 0)
        call_command('generate_data')
        self.assertGreater(Items.objects.count(), 0)