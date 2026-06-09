import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from core.models import Items


class Command(BaseCommand):
    help = 'Сгенерировать 50 записей тестовых данных (только если их меньше 50)'

    def handle(self, *args, **options):
        # Проверяем количество записей
        count = Items.objects.count()

        if count >= 50:
            self.stdout.write(self.style.WARNING(f'Записей уже {count}  (>=50). Пропускаем генерацию.'))
            return

        needed = 50 - count
        self.stdout.write(f'Добавляем {needed} новых записей...')

        names = ['Маршрут А', 'Маршрут Б', 'Маршрут В', 'Маршрут Г', 'Маршрут Д']

        for i in range(needed):
            Items.objects.create(
                date=datetime.now() - timedelta(days=random.randint(1, 365)),
                name=random.choice(names),
                quantity=random.randint(1, 100),
                distance=random.randint(1, 1000)
            )
        self.stdout.write(self.style.SUCCESS(f'УСПЕШНО сгенерировано. ВСЕГО: {Items.objects.count()} записей'))