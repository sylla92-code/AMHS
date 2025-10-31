from django.db import models

# Create your models here.
class Tableau(models.Model):
    numero_car= models.IntegerField()
    temperature = models.FloatField()
    tension = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.numero_car)