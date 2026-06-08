from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Items


class ItemsAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

        Items.objects.create(
            date='2026-01-02',
            name='Тестовый маршрут',
            quantity=99,
            distance=500,
        )
        Items.objects.create(
            date='2026-01-02',
            name='Другой маршрут',
            quantity=100,
            distance=505,
        )
        Items.objects.create(
            date='2026-03-04',
            name='Еще маршрут',
            quantity=111,
            distance=666,
        )

    def test_get_items_list(self):
        """Тест получения списка маршрутов"""
        response = self.client.get('/api/items/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 3)

    def test_get_single_item(self):
        """Тест получения одного маршрута"""
        item = Items.objects.first()
        response = self.client.get(f'/api/items/{item.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Тестовый маршрут')

    def test_create_item(self):
        """Тест создания маршрута"""
        data = {
            'date': '2026-01-03',
            'name': 'Новый маршрут',
            'quantity': 75,
            'distance': 400,
        }
        response = self.client.post('/api/items/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Items.objects.count(), 4)

    def test_update_item(self):
        """Тест обновления маршрута"""
        item = Items.objects.first()
        data = {'name': 'Обновленный маршрут'}
        response = self.client.patch(f'/api/items/{item.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        item.refresh_from_db()
        self.assertEqual(item.name, 'Обновленный маршрут')

    def test_delete_item(self):
        """Тест удаления маршрута"""
        item = Items.objects.first()
        response = self.client.delete(f'/api/items/{item.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Items.objects.count(), 2)

    def test_filter_by_name(self):
        """Тест фильтрации по названию"""
        response = self.client.get('/api/items/?name=Тестовый маршрут')
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['name'], 'Тестовый маршрут')

    def test_filter_by_quantity_min(self):
        """Тест фильтрации по минимальному количеству"""
        response = self.client.get('/api/items/?quantity__gte=100')
        self.assertEqual(response.data['count'], 2)

    def test_ordering_by_name(self):
        """Тест сортировки по названию"""
        response = self.client.get('/api/items/?ordering=name')
        self.assertEqual(response.data['results'][0]['name'], 'Другой маршрут')

    def test_pagination(self):
        """Тест пагинации"""
        # Создаём дополнительные записи для пагинации (больше 10)
        for i in range(15):
            Items.objects.create(
                date='2024-01-01',
                name=f'Маршрут {i}',
                quantity=i,
                distance=i * 10
            )
        response = self.client.get('/api/items/?page=2')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # На второй странице должна быть ссылка "next" только если есть страница 3
        # Всего записей: 3 + 15 = 18. По 10 на страницу: 2 страницы (1-10, 11-18)
        # На 2 странице нет следующей страницы, поэтому next = None
        # Проверяем, что пагинация работает
        self.assertIn('results', response.data)
        self.assertEqual(len(response.data['results']), 8)  # 18 - 10 = 8 на 2 странице