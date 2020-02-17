from django.db import models
from django.conf import settings
from clientes.models import Cliente
from medicamentos.models import Medicamentos
from django.db.models import signals


# Create your models here.
class Receta(models.Model):
    serie = models.IntegerField()
    numero = models.CharField(max_length=6)
    cliente = models.ForeignKey(Cliente, null=False, blank=False, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    emisor = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, blank=False, on_delete=models.CASCADE)

    class Meta:
        # no duplicate serie y numero juntos
        unique_together = (('serie', 'numero'),)

    def __str__(self):
        return U" %s- %s" % (self.serie, self.numero)


class DetalleReceta(models.Model):
    factura = models.ForeignKey(Receta, db_column='receta_id', related_name='receta', null=False, blank=False, on_delete=models.CASCADE)
    medicamento = models.ForeignKey(Medicamentos, db_column='medicamento_id', null=False, blank=False, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=40)
    precio = models.DecimalField(max_digits=6, decimal_places=2)
    cantidad = models.IntegerField()
    impuesto = models.DecimalField(max_digits=6, decimal_places=2)
    subtotal = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return u'%s' % self.descripcion

    def suma(self):
        return self.cantidad * self.medicamento.precio_venta


def update_stock(sender, instance, **kwargs):
    instance.medicamento.stock -= instance.cantidad
    instance.medicamento.save()


# register the signal
signals.post_save.connect(update_stock, sender=DetalleReceta, dispatch_uid="update_stock_count")
