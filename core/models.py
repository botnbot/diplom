from django.db import models

class Items (models.Model):
    date = models.DateField()
    name = models.CharField()
    quantity = models.DecimalField()
    distance = models.DecimalField()

