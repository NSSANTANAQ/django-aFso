from django.core.exceptions import ValidationError
from django.db.models import Sum
from django.db.models.signals import post_save
from autenticacion.models import Usuario
from django.db import models, transaction
from django.db.utils import IntegrityError
from django.contrib import messages
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Clientes(models.Model):
    cliente_id = models.AutoField(primary_key=True)
    cliente_ruc = models.CharField(max_length=13)
    cliente_razonsocial = models.CharField(max_length=255)
    cliente_direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    correo = models.CharField(max_length=150)

    usuario_creacion = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='clientescreado_por')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario_modificacion = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='clientesmodificado_por')
    fecha_modificacion = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.cliente_razonsocial

    class Meta:
        db_table = "clientes"
        verbose_name = "clientes"
        verbose_name_plural = "clientes"

class Presentacion(models.Model):
    presentacion_id = models.AutoField(primary_key=True)
    presentacion_detalle = models.CharField(max_length=150)

    usuario_creacion = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='presentacioncreado_por')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario_modificacion = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='presentacionmodificado_por')
    fecha_modificacion = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.presentacion_detalle

    class Meta:
        db_table = "presentacion"
        verbose_name = "presentacion"
        verbose_name_plural = "presentacion"

class Movimientoproductos(models.Model):
    mov_producto_id = models.AutoField(primary_key=True)
    mov_producto_tipo = models.CharField(max_length=200)
    mov_producto_nom = models.CharField(max_length=200)
    mov_producto_presentacion = models.ForeignKey(Presentacion, on_delete=models.CASCADE)
    mov_producto_fechaingreso = models.DateField()
    mov_producto_cantidad = models.PositiveIntegerField()
    mov_producto_precio = models.DecimalField(max_digits=10, decimal_places=2)
    mov_producto_observacion = models.CharField(max_length=300)


    usuario_creacion = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='movimientoproductoscreado_por')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario_modificacion = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='movimientoproductosmodificado_por')
    fecha_modificacion = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.mov_producto_nom


    class Meta:
        db_table = "Movimientoproductos"
        verbose_name = "Movimientoproductos"
        verbose_name_plural = "Movimientoproductos"


class Productos(models.Model):
    producto_id = models.AutoField(primary_key=True)
    producto_nom = models.CharField(max_length=200)
    producto_presentacion = models.ForeignKey(Presentacion, on_delete=models.CASCADE)
    producto_fechaingreso = models.DateField()
    producto_stock = models.PositiveIntegerField()
    producto_precio = models.DecimalField(max_digits=10, decimal_places=2)


    usuario_creacion = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='productocreado_por')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    usuario_modificacion = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name='productomodificado_por')
    fecha_modificacion = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.producto_nom


    class Meta:
        db_table = "Productos"
        verbose_name = "Productos"
        verbose_name_plural = "Productos"


class Factura(models.Model):
    ESTADOS = [
        ('AB', 'Abierta'),
        ('CE', 'Cerrada'),
        ('DV', 'Devuelta'),
    ]
    numero = models.CharField(max_length=20, blank=True, unique=True)
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tipo_pago = models.CharField(max_length=10, choices=[('EFECTIVO', 'EFECTIVO'), ('CREDITO', 'CREDITO')],default='EFECTIVO')
    estado = models.CharField(max_length=2, choices=ESTADOS, default='AB')

    ESTABLECIMIENTO = '001'
    PUNTO_EMISION = '001'

    def __str__(self):
        return f"Factura {self.numero}"

    def save(self, *args, **kwargs):
        if not self.numero:
            with transaction.atomic():
                last_factura = Factura.objects.select_for_update().order_by('-id').first()
                if last_factura and last_factura.numero:
                    last_number = int(last_factura.numero.split('-')[-1])
                    new_number = last_number + 1
                else:
                    new_number = 1
                self.numero = f"{self.ESTABLECIMIENTO}-{self.PUNTO_EMISION}-{new_number:08d}"
        super(Factura, self).save(*args, **kwargs)



class Configuracion(models.Model):
    iva = models.DecimalField(max_digits=5, decimal_places=2, default=0.15)  # IVA en porcentaje
    porcentaje_credito = models.DecimalField(max_digits=5, decimal_places=2, default=0.5)  # Porcentaje adicional para crédito

    def save(self, *args, **kwargs):
        if not Configuracion.objects.exists():
            super(Configuracion, self).save(*args, **kwargs)

class Gestionar_listado(models.Model):
    fecha_inicio = models.DateField()
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    pendiente = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pagado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.CharField(max_length=2, default='AB')

    def calcular_total(self):
        return self.gestion_listado.aggregate(total=Sum('total'))['total'] or 0

    def calcular_pagado(self):
        return self.gestion_listado.filter(estado='PG').aggregate(total_pagado=Sum('total'))['total_pagado'] or 0

    def calcular_pendiente(self):
        total = self.calcular_total()
        pagado = self.calcular_pagado()
        return total - pagado
class Gestionar_listado_detalle(models.Model):
    gestion = models.ForeignKey(Gestionar_listado, on_delete=models.CASCADE, related_name='gestion_listado')
    fecha_registro = models.DateField()
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE, related_name='producto_listado')
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=2, default='AB')
    d_factura = models.ForeignKey(Factura, on_delete=models.CASCADE, blank=True, null=True)

class FacturaDetalle(models.Model):
    factura = models.ForeignKey(Factura, related_name='lineas', on_delete=models.CASCADE)
    producto = models.ForeignKey(Productos, on_delete=models.CASCADE, related_name='producto')
    cantidad = models.PositiveIntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=2, default='PD')
    pedido_id = models.ForeignKey(Gestionar_listado_detalle, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.producto.producto_nom} - {self.cantidad} x {self.precio}"



