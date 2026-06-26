from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from core.models import Items

class FrontendViewsTest(TestCase):
    def setUp(self):
        self.item = Items.objects.create(
            name="Test Item",
            quantity=10,
            date=timezone.now().date(),
            distance=0
        )

    def test_index_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<html")

    def test_api_items_list(self):
        response = self.client.get('/api/items/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Item")