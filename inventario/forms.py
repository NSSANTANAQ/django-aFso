from django import forms
from django_select2.forms import Select2Widget

from inventario.models import Clientes,Productos,Presentacion,Gestionar_listado,Gestionar_listado_detalle, Movimientoproductos, Factura,FacturaDetalle,Configuracion

class BusquedaForm(forms.Form):
    solicitud = forms.CharField(max_length=100, required=False)
    apellido = forms.CharField(max_length=100, required=False)
    OPCIONES = [
        ('', ''),
        ('DIRECCIÓN ADMINISTRATIVA', 'DIRECCIÓN ADMINISTRATIVA'),

    ]
    area = forms.ChoiceField(choices=OPCIONES, required=False, label='Area',
                             widget=forms.Select(attrs={'class': ''}))

class BusquedaEmpleadoForm(forms.Form):
    fun_cedula= forms.CharField(max_length=100, required=False)
    fun_apelllido = forms.CharField(max_length=100, required=False)

class BusquedaProductoForm(forms.Form):
    producto= forms.CharField(max_length=100, required=False)

class BusquedaProductoMovimientoForm(forms.Form):
    producto = forms.CharField(max_length=100, required=False)
class BusquedaClienteForm(forms.Form):
   cliente_ruc = forms.CharField(max_length=100, required=False)
   cliente_razonsocial= forms.CharField(max_length=100, required=False)

class ReporteForm(forms.Form):
    fecha_desde = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    fecha_hasta = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    empleado_id = forms.IntegerField(label='ID', required=False)

class HorasForm(forms.Form):
    fecha_desde = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    fecha_hasta = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

class BusquedaHorasForm(forms.Form):
    fecha_desde = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    fecha_hasta = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    empleado_id = forms.IntegerField(label='ID', required=False)


class ClientesForm(forms.ModelForm):
    class Meta:
        model = Clientes
        fields = ['cliente_ruc', 'cliente_razonsocial', 'cliente_direccion', 'telefono', 'correo']


class PresentacionForm(forms.ModelForm):
    class Meta:
        model = Presentacion
        fields = ['presentacion_id', 'presentacion_detalle']



class ProductosForm(forms.ModelForm):

        class Meta:
            model = Productos
            fields = ['producto_nom', 'producto_presentacion', 'producto_fechaingreso','producto_stock', 'producto_precio']
            widgets = {
                'producto_fechaingreso': forms.DateInput(attrs={'type': 'date'}),
                'producto_presentacion': forms.Select(attrs={'class': 'select2'}),
            }

class MovproductoForm(forms.ModelForm):
    TIPO_CHOICES = [
        ('INGRESO', 'INGRESO'),
        ('EGRESO', 'EGRESO'),
    ]
    mov_producto_tipo = forms.ChoiceField(choices=TIPO_CHOICES, label='tipo de movimiento')
    mov_producto_precio = forms.DecimalField(max_digits=10, decimal_places=2, required=True)
    mov_producto_observacion = forms.CharField(label='Observación', widget=forms.Textarea(attrs={'name': 'body', 'rows': 10, 'cols': 20}))
    class Meta:
        model = Movimientoproductos
        fields = ['mov_producto_nom','mov_producto_presentacion', 'mov_producto_fechaingreso', 'mov_producto_precio' , 'mov_producto_cantidad','mov_producto_observacion']
        widgets = {
            'mov_producto_fechaingreso': forms.DateInput(attrs={'type': 'date'}),
            'mov_producto_nom': forms.Select(attrs={'class': 'select2'}),
        }

class MovproductoModificarForm(forms.ModelForm):
    TIPO_CHOICES = [
        ('INGRESO', 'INGRESO'),
        ('EGRESO', 'EGRESO'),
    ]
    mov_producto_tipo = forms.ChoiceField(choices=TIPO_CHOICES, label='tipo de movimiento')
    mov_producto_nom = forms.CharField(max_length=100)
    mov_producto_precio = forms.DecimalField(max_digits=10, decimal_places=2)
    mov_producto_observacion = forms.CharField(label='Observación', widget=forms.Textarea(attrs={'name': 'body', 'rows': 10, 'cols': 20}))

    class Meta:
        model = Movimientoproductos
        fields = ['mov_producto_nom','mov_producto_presentacion', 'mov_producto_fechaingreso', 'mov_producto_cantidad', 'mov_producto_precio' , 'mov_producto_observacion']


class FacturaForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = ['cliente']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'select2'}),
        }

class FacturaDetalleForm(forms.ModelForm):
    class Meta:
        model = FacturaDetalle
        fields = ['producto', 'cantidad']
        widgets = {
            'producto': forms.Select(attrs={'class': 'select2'}),
        }

class ConfiguracionForm(forms.ModelForm):
    class Meta:
        model = Configuracion
        fields = ['iva', 'porcentaje_credito']
        widgets = {
            'iva': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'max': '1'}),
            'porcentaje_credito': forms.NumberInput(attrs={'step': '0.01', 'min': '0', 'max': '1'}),
        }

class BuscareportForm(forms.Form):
    fecha_desde = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),required=False)
    fecha_hasta = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}),required=False)
    OPCIONES = [

        ('clientes', 'clientes'),
        ('productos', 'productos'),
        ('facturas', 'facturas'),
        ('movimientos', 'movimientos')

    ]
    reporte = forms.ChoiceField(choices=OPCIONES, label='Reporte',
                             widget=forms.Select(attrs={'class': ''}))

class GestionarlistadoForm(forms.ModelForm):
    class Meta:
        model = Gestionar_listado
        fields = ['fecha_inicio', 'cliente']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'cliente': forms.Select(attrs={'class': 'select2'}),
        }

class BuscarListadoForm(forms.Form):
    cliente = forms.CharField(max_length=200)

class GestionarlistadodetalleForm(forms.ModelForm):

    # d_factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    # id_producto = models.ForeignKey(FacturaDetalle, on_delete=models.CASCADE)

    class Meta:
        model = Gestionar_listado_detalle
        fields = ['fecha_registro', 'producto','cantidad','precio']
        widgets = {
            'fecha_registro': forms.DateInput(attrs={'type': 'date'}),
            'producto': forms.Select(attrs={'class': 'select2'}),
        }

class ListadoDetalleForm(forms.Form):
    fecha_desde = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    fecha_hasta = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))