from django.contrib import admin
from .models import DetalleReceta, Receta


# Register your models here.
class DetalleRecetaInline(admin.TabularInline):
    model = DetalleReceta


class RecetaAdmin(admin.ModelAdmin):
    raw_id_fields = ('cliente',)
    inlines = (DetalleRecetaInline,)
    exclude = ['emisor', ]

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.vendedor = request.user
        obj.save()


admin.site.register(Receta, RecetaAdmin)
