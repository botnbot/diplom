from django.test import TestCase
from django.urls import reverse
from core.models import Items

class FrontendViewsTest(TestCase):
    def setUp(self):
        self.item = Items.objects.create(name="Test Item", quantity=10)

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/index.html')

    def test_item_list_page(self):
        response = self.client.get(reverse('item_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Item")