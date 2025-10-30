from django.db import models

# Create your models here.
class Tableau(models.Model):
    id= models.IntegerField(primary_key=True)
    temperature = models.FloatField()
    tension = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)