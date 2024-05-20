from django.db import models

# En temperature_app/models.py

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    cedula = models.CharField(max_length=15, blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)

    # Solucionar el conflicto de related_name
    groups = models.ManyToManyField(
        "auth.Group",
        verbose_name="Groups",
        blank=True,
        help_text="The groups this user belongs to.",
        related_name="customuser_set",
        related_query_name="customuser",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name="User permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="customuser_set",
        related_query_name="customuser",
    )

class TemperatureData(models.Model):
    temperature = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Temperature: {self.temperature} °C - Timestamp: {self.timestamp}"
    
class Pulsacion(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    pulsaciones_por_minuto = models.IntegerField()

    def __str__(self):
        return f'{self.fecha} - {self.pulsaciones_por_minuto} bpm'

class Medicion(models.Model):
    humedad = models.FloatField()
    temperatura = models.FloatField()
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Medicion: Humedad={self.humedad}%, Temperatura={self.temperatura}°C"
    
class MedicionCompleto(models.Model):
    temperatura = models.FloatField()
    pulsaciones = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    collar_id = models.CharField(max_length=5000)  # Agrega la variable 'collar_id'
    nombre_vaca = models.CharField(max_length=100)

    def __str__(self):
        return f"ID: {self.id}, Nombre: {self.nombre_vaca}, Temperatura: {self.temperatura}, Pulsaciones: {self.pulsaciones}, Collar ID: {self.collar_id}, Fecha: {self.fecha_creacion}"