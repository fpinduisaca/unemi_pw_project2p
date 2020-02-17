from django.contrib import admin
from .models import *


# Register your models here.
# admin.site.register(Cliente)
@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('identificacion', 'nombres', 'apellidos', 'direccion', 'telefono')
    search_fields = ('identificacion', 'apellidos')
