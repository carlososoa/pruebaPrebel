from django.db import models

# Create your models here.

class Facturas(models.Model):
    codigo_producto = models.CharField(max_length=50, db_collation='Modern_Spanish_CI_AI', blank=True, null=True)
    nombre_producto = models.CharField(max_length=50, db_collation='Modern_Spanish_CI_AI', blank=True, null=True)
    cantidad = models.IntegerField(blank=True, null=True)
    fecha_compra = models.DateField(blank=True, null=True)
    numero_factura = models.CharField(max_length=50, db_collation='Modern_Spanish_CI_AI', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'FACTURAS'
