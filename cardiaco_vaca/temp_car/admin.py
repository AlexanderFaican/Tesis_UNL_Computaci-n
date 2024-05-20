from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
# Register your models here.

admin.site.register(TemperatureData)
admin.site.register(Pulsacion)
admin.site.register(Medicion)
admin.site.register(MedicionCompleto)