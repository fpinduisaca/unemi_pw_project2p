from django.db import models


# Create your models here.
class Cliente(models.Model):
    identificacion = models.CharField(max_length=10, unique=True, null=False, blank=False)
    nombres = models.CharField(max_length=60, null=False, blank=False)
    apellidos = models.CharField(max_length=100, null=False, blank=False)
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, verbose_name='Telefono')

    def __str__(self):
        return self.nombres
