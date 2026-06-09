from django.db import models

class Items (models.Model):
    date = models.DateField()
    name = models.CharField(max_length=255)
    quantity = models.IntegerField(max_length=4)
    distance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.date}"

