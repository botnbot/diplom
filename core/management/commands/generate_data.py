import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from core.models import Items


class Command(BaseCommand):
    help = 'Generate random data for Items'

    def handle(self, *args, **options):
        names = ['Маршрут А', 'Маршрут Б', 'Маршрут В', 'Маршрут Г', 'Маршрут Д']

        for i in range(50):
            Items.objects.create(
                date=datetime.now() - timedelta(days=random.randint(1, 365)),
                name=random.choice(names),
                quantity=random.randint(1, 100),
                distance=random.randint(1, 1000)
            )
        self.stdout.write(self.style.SUCCESS('Successfully generated data'))