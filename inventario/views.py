import datetime
from datetime import date
from decimal import Decimal, ROUND_HALF_UP
from django.db.models import Q, Sum
from django.http import JsonResponse, HttpResponseNotFound, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db import models
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.conf import settings
from .forms import (ProductosForm,BusquedaClienteForm,BusquedaProductoForm,GestionarlistadodetalleForm,
                    GestionarlistadoForm, MovproductoModificarForm,ListadoDetalleForm, PresentacionForm,BuscarListadoForm, MovproductoForm,HorasForm,BusquedaProductoMovimientoForm,ClientesForm,ConfiguracionForm,BuscareportForm)
from .models import Productos, Movimientoproductos, Clientes,Presentacion, Gestionar_listado,Gestionar_listado_detalle, Factura, FacturaDetalle,Configuracion, Gestionar_listado_detalle
from django.shortcuts import render, HttpResponseRedirect, reverse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import inlineformset_factory
from .models import Factura, FacturaDetalle
from .forms import FacturaForm, FacturaDetalleForm
from dal import autocomplete
import json
from django_select2.views import AutoResponseView
from django.http import JsonResponse
from collections import OrderedDict
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from autenticacion.models import Usuario
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='login1')
def menu_sistemas(request):
    return render(request, 'menu_sistema.html')

# def buscar_productos(request):
#     if request.method == 'GET' and 'term' in request.GET:
#
#         term = request.GET.get('term')
#         print(term)
#         productos = Productos.objects.filter(producto_nom__icontains=term)
#         print(productos)
#         nombres_productos = list(producto.producto_nom for producto in productos)
#         print(nombres_productos)
#         return JsonResponse(nombres_productos, safe=False)
#     return JsonResponse([], safe=False)
@login_required(login_url='login1')
def buscar_productos(request):
    term = request.GET.get('term', '')
    productos = Productos.objects.filter(producto_nom__icontains=term).values_list('producto_nom', flat=True)
    print(productos)
    return JsonResponse(list(productos), safe=False)

@login_required(login_url='login1')
def buscar_clientes(request):
    term = request.GET.get('term', '')
    clientes = Clientes.objects.filter(cliente_razonsocial__icontains=term).values_list('cliente_razonsocial', flat=True)
    print(clientes)
    return JsonResponse(list(clientes), safe=False)

@login_required(login_url='login1')
def consulta_producto_stock(request):
    if request.method == 'POST':
        form = BusquedaProductoForm(request.POST)
        if form.is_valid():
            fecha_desde = form.cleaned_data['producto']

            resultados = Productos.objects.filter(producto_nom__icontains=fecha_desde)

        else:
            resultados = []

    else:
        form = BusquedaProductoForm()
        resultados= Productos.objects.all()

    # count = Solicitudes.objects.filter(estado=1).count()
    return render(request, 'consulta_producto_stock.html', {'form': form, 'resultados': resultados})
@login_required(login_url='login1')
def crear_producto_stock(request):
    if request.method == "POST":
        Agregarfuncionarios = ProductosForm(request.POST, request.FILES)
        if Agregarfuncionarios.is_valid():
            producto_stock = Agregarfuncionarios.cleaned_data['producto_stock']
            producto_precio = Agregarfuncionarios.cleaned_data['producto_precio']
            print(producto_stock)
            if producto_stock == 0 or producto_precio == 0:
                if producto_precio == 0:
                    messages.error(request, 'El precio no debe ser 0 ¡importante!')
                if producto_stock == 0:
                    messages.error(request, 'Stock Minimo 1 ¡importante!.')
                return redirect('crear_producto_stock')

            nuevo_registro = Agregarfuncionarios.save(commit=False)
            nuevo_registro.usuario_creacion = request.user
            nuevo_registro.usuario_modificacion = request.user
            nuevo_registro.save()

            return HttpResponseRedirect(reverse('consulta_producto_stock'))

        else:
            crearform = ProductosForm()

    else:
        preform = PresentacionForm()
        crearform= ProductosForm()
        resultados_pre = Presentacion.objects.all()
    return render(request, 'crear_producto_stock.html',{'form':crearform,'resultados_pre':resultados_pre,'preform':preform})
@login_required(login_url='login1')
def crear_presentacion(request):
    if request.method == "POST":
        Agregarfuncionarios = PresentacionForm(request.POST, request.FILES)
        if Agregarfuncionarios.is_valid():
            nuevo_registro = Agregarfuncionarios.save(commit=False)
            nuevo_registro.usuario_creacion = request.user
            nuevo_registro.usuario_modificacion = request.user
            nuevo_registro.save()
            return HttpResponseRedirect(reverse('crear_producto_stock'))

        else:
            crearform = PresentacionForm()

    else:
        crearform= PresentacionForm()

    return render(request, 'crear_producto_presentacion.html',{'form':crearform})

def obtener_datos_actualizados(request):
    if request.method == 'GET':
        presentaciones = Presentacion.objects.all().values('presentacion_id', 'presentacion_detalle')
        data = list(presentaciones)  # Convertir QuerySet a lista
        return JsonResponse({'success': True, 'presentaciones': data})
    return JsonResponse({'success': False, 'error': 'Método no permitido'}, status=405)

@login_required(login_url='login1')
def modificar_presentacion(request):
    if request.method == 'POST':
        try:
            actualizaciones = []
            for key, value in request.POST.items():
                if key.startswith('save_'):
                    presentacion_id = key.split('_')[1]
                    presentacion_detalle = request.POST.get(f'presentacion_{presentacion_id}')

                    presentacion = get_object_or_404(Presentacion, presentacion_id=presentacion_id)
                    presentacion.presentacion_detalle = presentacion_detalle
                    presentacion.save()

                    actualizaciones.append({
                        'presentacion_id': presentacion.presentacion_id,
                        'presentacion_detalle': presentacion.presentacion_detalle,
                    })

                elif key.startswith('delete_'):
                    presentacion_id = key.split('_')[1]
                    presentacion = get_object_or_404(Presentacion, presentacion_id=presentacion_id)
                    presentacion.delete()

                    actualizaciones.append({
                        'presentacion_id': presentacion_id,
                        'deleted': True,
                    })
            return JsonResponse({
                'status': 'success',
                'message': 'Operación completada correctamente.',
                'actualizaciones': actualizaciones,
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e),
            })
@login_required(login_url='login1')
def consulta_producto_movimiento(request):
    if request.method == 'POST':
        form = BusquedaProductoMovimientoForm(request.POST)
        if form.is_valid():
            producto = form.cleaned_data['producto']
            resultados = Movimientoproductos.objects.filter( mov_producto_nom=producto)


    else:
        form = BusquedaProductoMovimientoForm()
        resultados= Movimientoproductos.objects.all()

    # count = Solicitudes.objects.filter(estado=1).count()
    return render(request, 'consultar_movimiento_producto.html', {'form': form, 'resultados': resultados})

@login_required(login_url='login1')
def modificar_producto_movimiento(request, pk):
    producto_movimiento = get_object_or_404(Movimientoproductos, pk=pk)
    if request.method == "POST":
        form = MovproductoModificarForm(request.POST, instance=producto_movimiento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Movimiento Modificado Correctamente')
            return redirect('consulta_producto_movimiento')  # Redireccionar a donde quieras después de modificar
    else:
        form = MovproductoModificarForm(instance=producto_movimiento)

        return render(request, 'crear_producto_movimiento.html',
                      {'form': form})
@login_required(login_url='login1')
def crear_producto_movimiento(request):
    if request.method == 'POST':
        form = MovproductoForm(request.POST)
        if form.is_valid():
            tipo_movimiento = form.cleaned_data['mov_producto_tipo']
            cantidad = form.cleaned_data['mov_producto_cantidad']
            precio = form.cleaned_data['mov_producto_precio']
            presentacion = form.cleaned_data['mov_producto_presentacion']
            fechaingreso = form.cleaned_data['mov_producto_fechaingreso']
            producto_id = form.cleaned_data['mov_producto_nom']
            observacion = form.cleaned_data['mov_producto_observacion']
            print(producto_id)
            print(precio)

            try:
                producto = Productos.objects.get(producto_nom=producto_id)
                productos = get_object_or_404(Productos, producto_nom=producto_id)
                productos.producto_precio = precio
                productos.save()
                # Realizar operaciones con el producto encontrado
            except ObjectDoesNotExist:
                producto = None
            if tipo_movimiento == 'INGRESO':
                producto.producto_stock += cantidad
            else:
                producto.producto_stock -= cantidad

            # Actualizar la fecha de ingreso del producto
            producto.producto_fechaingreso = fechaingreso
            producto.save()

            Productos.objects.update(
                producto_precio = precio
            )

            # Registrar el movimiento
            Movimientoproductos.objects.create(
                mov_producto_tipo=tipo_movimiento,
                mov_producto_cantidad=cantidad,
                mov_producto_nom=producto,
                mov_producto_fechaingreso = fechaingreso,
                mov_producto_presentacion= presentacion,
                mov_producto_precio = precio,
                mov_producto_observacion= observacion,
                usuario_creacion_id= request.user.id,
                usuario_modificacion_id= request.user.id
            )

            return redirect('consulta_producto_movimiento')
    else:
        form = MovproductoForm()

    return render(request, 'crear_producto_movimiento.html', {'form': form})

def obtener_precio_producto_presentacion(request):
    producto_id = request.GET.get('producto_id')
    presentacion_id = request.GET.get('presentacion_id')
    print(producto_id,presentacion_id)
    if producto_id and presentacion_id:
        try:
            presentacion = Productos.objects.get(producto_id=producto_id, producto_presentacion_id=presentacion_id)
            return JsonResponse({'precio': presentacion.producto_precio}, status=200)
        except Presentacion.DoesNotExist:
            return JsonResponse({'error': 'Presentación no encontrada'}, status=404)

    return JsonResponse({'error': 'Faltan parámetros'}, status=400)





@login_required(login_url='login1')
def consulta_factura(request):
    if request.method == 'POST':
        form = HorasForm(request.POST)
        if form.is_valid():
            fecha_desde = form.cleaned_data['fecha_desde']
            fecha_hasta = form.cleaned_data['fecha_hasta']
            resultados = Factura.objects.filter(fecha__range=(fecha_desde, fecha_hasta))
        else:
            messages.success(request,'Resultados')
            resultados = []
    else:
        form = HorasForm()
        resultados = Factura.objects.all().order_by('-id')

    return render(request, 'consulta_factura.html', {'form': form, 'resultados': resultados})
# def crear_factura(request):
#     if request.method == 'POST':
#         factura_form = FacturaForm(request.POST)
#         if factura_form.is_valid():
#             factura = factura_form.save()
#             total = 0
#             factura.total = total
#             factura.save()
#
#             return redirect('crear_factura_producto', )
#     else:
#         factura_form = FacturaForm()
#
#     return render(request, 'crear_nueva_factura.html', {
#         'factura_form': factura_form
#     })
@login_required(login_url='login1')
def crear_factura(request):

    if request.method == 'POST':
        factura_abierta = Factura.objects.filter(estado='AB').first()

        if factura_abierta:
            form = FacturaForm()
            messages.error(request, 'Tiene una factura pendiente.')
            return render(request, 'crear_nueva_factura.html',
                          {'factura_form': form, 'factura_abierta': factura_abierta,'show_modal': True})

        form = FacturaForm(request.POST)
        if form.is_valid():
            factura = form.save()
            total = 0
            factura.total = total
            factura.save()
            return redirect('crear_factura_producto', factura.id)
    else:

        factura_abierta = Factura.objects.filter(estado='AB').first()

        form = FacturaForm()
    return render(request, 'crear_nueva_factura.html', {'factura_form': form,'factura_abierta': factura_abierta})

@login_required(login_url='login1')
def eliminar_factura(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id)
    detalles = FacturaDetalle.objects.filter(factura=factura)
    pedidos = Gestionar_listado_detalle.objects.filter(d_factura_id=factura_id)


    if pedidos.exists():

        for pedido in pedidos:
            print(pedido.gestion_id)
            p_pedidos = Gestionar_listado.objects.get(id=pedido.gestion_id)
            pedido.d_factura_id = None
            pedido.estado = 'AB'
            pedido.save()
            p_pedidos.estado = 'AB'
            p_pedidos.save()


    if detalles.exists():
        for detalle in detalles:
            producto = detalle.producto
            producto.producto_stock += detalle.cantidad
            producto.save()

        factura.estado = 'DV'  # Estado que indica que la factura ha sido devuelta
        factura.save()

        messages.success(request, 'La factura ha sido devuelta y los productos han sido reingresados al stock.')
    else:
        messages.error(request, 'No se puede devolver la factura porque no tiene productos relacionados.')

    return redirect('consulta_factura')

@login_required(login_url='login1')
def crear_factura_producto(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id)
    lineas = factura.lineas.all()
    configuracion = Configuracion.objects.first()
    if request.method == 'POST':
        form = FacturaDetalleForm(request.POST)
        print(form)
        if form.is_valid():
            cantidad = form.cleaned_data['cantidad']
            print(cantidad)
            if cantidad == 0:
                messages.error(request, 'La cantidad no puede ser a 0.')
                return redirect('crear_factura_producto', factura_id)


            producto = form.cleaned_data['producto']
            print(producto)
            producto = get_object_or_404(Productos, producto_nom=producto)
            print(producto.producto_stock)
            linea_existente = factura.lineas.filter(producto=producto, factura = factura_id, estado = 'N').first()

            if linea_existente:
                nueva_cantidad = linea_existente.cantidad + cantidad
            else:
                nueva_cantidad = cantidad

            # Verificar el stock disponible
            if nueva_cantidad > producto.producto_stock:
                messages.error(request,
                               f'El stock del producto "{producto.producto_nom}" es menor a la cantidad total ingresada. Stock actual: {producto.producto_stock}.')
                return redirect('crear_factura_producto', factura_id)

            precio_unitario = producto.producto_precio  # Asegúrate de que este campo exista en tu modelo de Producto
            nuevo_precio_total = precio_unitario * nueva_cantidad

            # Actualizar o crear la línea de la factura
            if linea_existente:
                linea_existente.cantidad = nueva_cantidad
                linea_existente.total = nuevo_precio_total # Asegúrate de que este campo exista en tu modelo de FacturaDetalle
                linea_existente.estado = 'N'
                linea_existente.save()
                recalcular_total_factura(factura)
                return redirect('crear_factura_producto', factura_id)


            # if producto.producto_stock < cantidad:
            #     messages.error(request, f'El stock del producto "{producto.producto_nom}" es menor a la cantidad ingresada. Stock actual: {producto.producto_stock}.')
            #     return redirect('crear_factura_producto', factura_id)
            if producto.producto_stock == 0:
                messages.error(request, f'No queda stock de este producto: {producto}')
                return redirect('crear_factura_producto', factura_id)

            linea = form.save(commit=False)
            linea.estado = 'N'
            linea.precio = linea.producto.producto_precio
            linea.factura = factura
            linea.total = linea.cantidad * linea.producto.producto_precio
            linea.save()
            recalcular_total_factura(factura)
            return redirect('crear_factura_producto', factura_id)
    else:
        form = FacturaDetalleForm()
        factura = get_object_or_404(Factura, id=factura_id)
        print(factura.cliente)
        resultados = Gestionar_listado_detalle.objects.filter(gestion__cliente__cliente_razonsocial = factura.cliente).order_by('fecha_registro')

        # Obtener el valor del IVA desde la configuración
        configuracion = Configuracion.objects.first()
        IVA_PERCENTAGE = Decimal(configuracion.iva)
        subtotal = factura.total

        # Calcular el IVA y el total
        iva = subtotal * IVA_PERCENTAGE
        total_con_iva = subtotal + iva

        subtotal = subtotal.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        iva = iva.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        total_con_iva = total_con_iva.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        # Pasar los valores al contexto

        grouped_resultados = OrderedDict()
        for resultado in resultados:
            stock_disponible = resultado.producto.producto_stock
            fecha = resultado.fecha_registro
            if fecha not in grouped_resultados:
                grouped_resultados[fecha] = []
            grouped_resultados[fecha].append({
        'resultado': resultado,
        'stock_disponible': stock_disponible,
    })

        context = {
            'factura': factura,
            'iva': iva,
            'total':  total_con_iva,
            'form': form,
            'lineas': lineas,
            'grouped_resultados': dict(grouped_resultados),
        }

    return render(request, 'crear_factura_añadir_producto.html', context )

def actualizar_tipo_pago(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id)
    if request.method == 'POST':
        tipo_pago = request.POST.get('tipo_pago')
        factura.tipo_pago = tipo_pago
        factura.save()
        try:
            actualizar_precios_lineas_factura(request, factura)
            messages.success(request, '¡Precios actualizados correctamente!')
        except Exception as e:
            messages.error(request, '¡Primero Añada los Productos!')

    return redirect('crear_factura_producto', factura_id=factura_id)

def actualizar_precios_lineas_factura(request,factura):
    lineas = FacturaDetalle.objects.filter(factura=factura.id)

    configuracion = Configuracion.objects.first()
    for linea in lineas:
        credito = Decimal(configuracion.porcentaje_credito)
        if factura.tipo_pago == 'CREDITO':
            if linea.estado == 'PD':
                print(linea.pedido_id.precio)
                credito = linea.pedido_id.precio * credito
                print(credito)
                linea.precio = linea.pedido_id.precio + credito
                linea.total = linea.precio * linea.cantidad
                print(linea.total)
                messages.success(request, 'Se actualizo la forma de pago')
            else:
                print(linea.producto.producto_precio)
                credito = linea.producto.producto_precio * credito
                print(credito)
                linea.precio = linea.producto.producto_precio + credito
                linea.total = linea.precio * linea.cantidad
                print(linea.total)
                messages.success(request, 'Se actualizo la forma de pago')

        else:
            if linea.estado == 'PD':
                print(linea.pedido_id.precio)
                linea.precio = linea.pedido_id.precio
                print(linea.precio)
                linea.total = linea.precio * linea.pedido_id.cantidad
                print(linea.total)
                messages.success(request, 'Se actualizo la forma de pago')
            else:
                print(linea.producto.producto_precio)
                linea.precio = linea.producto.producto_precio
                print(credito)
                linea.total = linea.precio * linea.cantidad
                print(linea.precio)
                messages.success(request, 'Se actualizo la forma de pago')

        linea.save()
    recalcular_total_factura(factura)

def recalcular_total_factura(factura):
    total = sum(linea.total for linea in FacturaDetalle.objects.filter(factura=factura.id))
    print(total)
    factura.total = total
    factura.save()
@login_required(login_url='login1')
def eliminar_producto_factura(request, producto_id):

    # Obtener la instancia del detalle de la factura o mostrar un error 404 si no existe
    detalle = get_object_or_404(FacturaDetalle, id=producto_id)
    print(detalle.pedido_id_id)
    if detalle.estado == 'PD':
        pedido = get_object_or_404(Gestionar_listado_detalle, id=detalle.pedido_id_id)
        pedido.estado = 'AB'
        pedido.d_factura_id = None
        pedido.save()

    # Obtener la factura asociada
    factura = detalle.factura
    # Eliminar el detalle de la factura
    detalle.delete()
    # Recalcular el total de la factura
    total_nuevo = sum(linea.total for linea in factura.lineas.all())
    factura.total = total_nuevo
    factura.save()
    print(factura.id)
    # Redirigir a una página después de la eliminación
    return redirect('crear_factura_producto', factura.id)
@login_required(login_url='login1')
def finalizar_factura(request, factura_id):
    factura = get_object_or_404(Factura, id=factura_id)
    lineas = factura.lineas.all()
    almenosuno = FacturaDetalle.objects.filter(factura_id=factura_id).exists()
    print(almenosuno)
    if almenosuno == True:
        for linea in factura.lineas.all():
            linea.estado = 'CE'
            linea.save()
            producto = linea.producto
            producto.producto_stock -= linea.cantidad
            producto.save()
        factura.estado = 'CE'
        factura.save()
        messages.success(request, 'La factura ha sido finalizada con éxito.')
        return redirect('consulta_factura')
    else:
        messages.error(request, 'No se puede finalizar la factura porque no se ha facturado ningún producto.')
        form = FacturaDetalleForm()
    return render(request, 'crear_factura_añadir_producto.html', {'factura': factura, 'form': form, 'lineas': lineas})

@login_required(login_url='login1')
def imprimir_factura(request, id):
    print(id)
    configuracion = Configuracion.objects.first()
    IVA_PERCENTAGE = Decimal(configuracion.iva)
    print(IVA_PERCENTAGE)
    # Obtén el registro de la base de datos según el ID
    factura = get_object_or_404(Factura, id=id)
    print(factura)

    factura_sin = factura.numero.replace('-', '')
    detalles = FacturaDetalle.objects.filter(factura_id=id).all()

    detalles_con_totales = []
    subtotal = Decimal('0.00')
    for detalle in detalles:
        total = detalle.cantidad * detalle.precio
        detalles_con_totales.append({
            'producto': detalle.producto,
            'cantidad': detalle.cantidad,
            'precio': detalle.precio,
            'total': total
        })
        subtotal += total

    iva = subtotal * IVA_PERCENTAGE
    total_con_iva = subtotal + iva

    # Redondear los valores monetarios a 2 decimales
    subtotal = subtotal.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    iva = iva.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    total_con_iva = total_con_iva.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    fecha_actual = date.today()
    base_url = request.build_absolute_uri('/')
    # Renderiza la plantilla con los datos del registro
    context = {
        'MEDIA_URL': request.build_absolute_uri('/'),
        'factura': factura,
        'factura_sin':factura_sin,
        'detalles': detalles_con_totales,
        'subtotal': subtotal,
        'iva': iva,
        'total_con_iva': total_con_iva,
        'fecha_actual': fecha_actual
    }

    template_path = 'imprimir_factura.html'
    # Renderiza la plantilla con el contexto
    template = get_template(template_path)
    rendered_html = template.render(context)

    # Crea un buffer en memoria para guardar el PDF
    response = BytesIO()
    pdf_status = pisa.CreatePDF(BytesIO(rendered_html.encode("utf-8")), dest=response, encoding='utf-8')

    # Verifica si hubo errores al generar el PDF
    if pdf_status.err:
        return HttpResponse('Hubo un error al generar el PDF', status=500)

    # Devuelve el PDF como una respuesta HTTP para descargar o mostrar en el navegador
    response = HttpResponse(response.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=Factura-{factura.numero}.pdf'
    return response
def buscar_productos_2(request):
    if request.is_ajax():
        term = request.GET.get('term', '')
        productos = Productos.objects.filter(nombre__icontains=term)
        results = []
        for producto in productos:
            producto_json = {}
            producto_json['id'] = producto.id
            producto_json['label'] = producto.nombre
            producto_json['value'] = producto.nombre
            producto_json['precio'] = str(producto.precio)
            results.append(producto_json)
        data = json.dumps(results)
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'error': 'Not an AJAX request'}, status=400)


@login_required(login_url='login1')
def consulta_cliente(request):
    if request.method == 'POST':
        form = BusquedaClienteForm(request.POST)
        if form.is_valid():
            ruc = form.cleaned_data['cliente_ruc']
            razon = form.cleaned_data['cliente_razonsocial']
            resultados = Clientes.objects.filter(Q(cliente_ruc__contains=ruc),Q(cliente_razonsocial__contains=razon))

        else:
            resultados = []

    else:
        form = BusquedaClienteForm()
        resultados= Clientes.objects.all()

    # count = Solicitudes.objects.filter(estado=1).count()
    return render(request, 'consultar_cliente.html', {'form': form, 'resultados': resultados})
@login_required(login_url='login1')
def crear_cliente(request):
    if request.method == "POST":
        Agregarcliente = ClientesForm(request.POST, request.FILES)
        if Agregarcliente.is_valid():
            nuevo_registro = Agregarcliente.save(commit=False)
            nuevo_registro.usuario_creacion = request.user
            nuevo_registro.usuario_modificacion = request.user
            now = timezone.now()
            nuevo_registro.fecha_creacion = now  # Asigna la fecha de creación con la zona horaria local
            nuevo_registro.fecha_modificacion = now # Asigna la fecha de modificación con la zona horaria local
            nuevo_registro.save()
            return HttpResponseRedirect(reverse('consulta_cliente'))

        else:
            crearform = ClientesForm()

    else:
        crearform= ClientesForm()

    return render(request, 'crear_cliente.html',{'form':crearform})


class ProductosAutocomplete(autocomplete.Select2QuerySetView):
    def get(self, request, *args, **kwargs):
        term = request.GET.get('q', '')
        productos = Productos.objects.filter(producto_nom__icontains=term)
        results = [{'id': producto.producto_id, 'text': producto.producto_nom} for producto in productos]
        return JsonResponse({'results': results})


class ClientesAutocomplete(AutoResponseView):

    def get(self, request, *args, **kwargs):
        term = request.GET.get('q', '')
        clientes = Clientes.objects.filter(cliente_razonsocial__icontains=term)
        results = [{'id': cliente.cliente_id, 'text': cliente.cliente_razonsocial} for cliente in clientes]
        return JsonResponse({'results': results})

@login_required(login_url='login1')
def configuracion_view(request):
    configuracion = Configuracion.objects.first()
    if request.method == 'POST':
        form = ConfiguracionForm(request.POST, instance=configuracion)
        if form.is_valid():
            form.save()
            messages.success(request,'Configuracion Guardada con Exito.')
            return redirect('configuracion_view')
    else:
        form = ConfiguracionForm(instance=configuracion)
    return render(request, 'configuracion.html', {'form': form})
@login_required(login_url='login1')
def reportes_generales(request):
    if request.method == 'POST':
        form = BuscareportForm(request.POST)
        if form.is_valid():
            fecha_desde = form.cleaned_data['fecha_desde']
            fecha_hasta = form.cleaned_data['fecha_hasta']
            reporte = form.cleaned_data['reporte']
            print(reporte)
            resultado = generar_reporte(fecha_desde, fecha_hasta, reporte)
            print(resultado)
            template_path = f'reporte_{reporte}.html'
            print(template_path)
            hoy = timezone.localtime(timezone.now()).date()
            base_url = request.build_absolute_uri('/')
            # Renderiza la plantilla con los datos del registro
            context = {
                'MEDIA_URL': request.build_absolute_uri('/'),
                'resultado': resultado,
                'hoy': hoy,
            }
            template = get_template(template_path)
            rendered_html = template.render(context)

            # Crea un buffer en memoria para guardar el PDF
            response_buffer = BytesIO()
            pdf_status = pisa.CreatePDF(BytesIO(rendered_html.encode("utf-8")), dest=response_buffer, encoding='utf-8')

            # Verifica si hubo errores al generar el PDF
            if pdf_status.err:
                return HttpResponse('Hubo un error al generar el PDF', status=500)

            # Devuelve el PDF como una respuesta HTTP para descargar o mostrar en el navegador
            response = HttpResponse(response_buffer.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename=Reporte.pdf'
            return response

            # rendered_html = render(request, template_path, context)
            # # Genera el PDF con WeasyPrint
            # pdf = HTML(string=rendered_html.content, base_url=base_url).write_pdf()
            #
            # # Devuelve el PDF como una respuesta HTTP para descargar
            # response = HttpResponse(pdf, content_type='application/pdf')
            # response['Content-Disposition'] = f'inline; filename=Reporte.pdf'
            # return response

        else:
            print('No se puede')

    else:
        form = BuscareportForm()

    return render(request, 'reporte_general.html',
                  {'form': form})


def generar_reporte(fecha_desde, fecha_hasta, reporte):
    if reporte == 'clientes':
        clientes = Clientes.objects.all()
        hoy = timezone.localtime(timezone.now()).date()

        clientes_nuevos = []
        clientes_anteriores = []

        for cliente in clientes:
            fecha_creacion_local = timezone.localtime(cliente.fecha_creacion).date()
            if fecha_creacion_local == hoy:
                clientes_nuevos.append(cliente)
            else:
                clientes_anteriores.append(cliente)

        data = {
            'clientes_nuevos': clientes_nuevos,
            'clientes_anteriores': clientes_anteriores,
        }
        print("Datos para Clientes:", data)

    elif reporte == 'productos':
        productos = Productos.objects.all()
        hoy = timezone.localtime(timezone.now()).date()

        productos_nuevos = []
        productos_anteriores = []

        for producto in productos:
            fecha_creacion_local = timezone.localtime(producto.fecha_creacion).date()
            if fecha_creacion_local == hoy:
                productos_nuevos.append(producto)
            else:
                productos_anteriores.append(producto)

        data = {
            'productos_nuevos': productos_nuevos,
            'productos_anteriores': productos_anteriores,
        }
        print("Datos para Productos:", data)

    elif reporte == 'facturas':
        # Convertimos las fechas desde y hasta en objetos de tipo date si no lo están
        # fecha_desde = timezone.make_aware(fecha_desde, timezone.get_current_timezone()).date()
        # fecha_hasta = timezone.make_aware(fecha_hasta, timezone.get_current_timezone()).date()

        # Filtramos las facturas dentro del rango de fechas
        facturas = Factura.objects.filter(fecha__range=(fecha_desde, fecha_hasta))
        credito = facturas.filter(tipo_pago='CREDITO',estado='CE')
        efectivo = facturas.filter(tipo_pago='EFECTIVO', estado='CE')
        total = facturas.filter(estado='CE')

        total_credito = credito.aggregate(total=models.Sum('total'))['total']
        total_efectivo = efectivo.aggregate(total=models.Sum('total'))['total']
        print(total_credito)
        print(total_efectivo)
        total = total.aggregate(total=models.Sum('total'))['total']
        print(total)

        data = {
            'facturas': facturas,
            'total_credito': total_credito,
            'total_efectivo': total_efectivo,
            'total': total,
        }
        print("Datos para Facturas Devueltas:", data)

    elif reporte == 'movimientos':
        movimientos = Movimientoproductos.objects.filter(mov_producto_fechaingreso__range=(fecha_desde, fecha_hasta))
        hoy = timezone.localtime(timezone.now()).date()

        movimientos_nuevos = []
        movimientos_anteriores = []

        for movimiento in movimientos:
            fecha_creacion_local = timezone.localtime(movimiento.fecha_creacion).date()
            if fecha_creacion_local == hoy:
                movimientos_nuevos.append(movimiento)
            else:
                movimientos_anteriores.append(movimiento)

        data = {
            'productos_nuevos': movimientos_nuevos,
            'productos_anteriores': movimientos_anteriores,
        }
        print("Datos para Productos:", data)
    else:
        print('Tipo de reporte no válido')
        data = {}

    return data

@login_required(login_url='login1')
def modificar_clientes(request, pk):
    cliente = get_object_or_404(Clientes, pk=pk)
    if request.method == "POST":
        form = ClientesForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente Modificado Correctamente')
            return redirect('consulta_cliente')  # Redireccionar a donde quieras después de modificar
    else:
        form = ClientesForm(instance=cliente)

        return render(request, 'crear_cliente.html',
                      {'form': form})
@login_required(login_url='login1')
def eliminar_clientes(request, pk):
    cliente = get_object_or_404(Clientes, pk=pk)
    cliente.delete()
    messages.success(request, 'Cliente eliminado Correctamente')
    return redirect('consulta_cliente')

@login_required(login_url='login1')
def modificar_productos(request, pk):
    cliente = get_object_or_404(Productos, pk=pk)
    if request.method == "POST":
        form = ProductosForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto Modificado Correctamente')
            return redirect('consulta_producto_stock')  # Redireccionar a donde quieras después de modificar
    else:
        form = ProductosForm(instance=cliente)

        return render(request, 'crear_producto_stock.html',
                      {'form': form})

def pantalla_carga(request, id):
    return render(request, 'pagina_carga.html', {'factura_id': id})

@login_required(login_url='login1')
def gestionar_perfil(request):
    return render(request, 'gestionar_perfil.html')
@login_required(login_url='login1')
def cambiar_password(request):
    print(request.user.id)
    user = Usuario.objects.get(id = request.user.id)
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Constraseña cambiada con Exito!,Inicia Sesión')
            # Redirige a una página de confirmación o muestra un mensaje de éxito
            return redirect('login1')
    else:
        form = SetPasswordForm(user)
    return render(request, 'password_reset_confirm.html', {'form': form})

@login_required(login_url='login1')
def gestionar_listado(request):
    resultados = Gestionar_listado.objects.all()
    for gestion in resultados:
        gestion.total = gestion.calcular_total()
        gestion.pagado = gestion.calcular_pagado()
        gestion.pendiente = gestion.calcular_pendiente()
        gestion.save()
        verificar_estado_gestion(gestion.id)

    if request.method == 'POST':
        form = BuscarListadoForm(request.POST)
        if form.is_valid():
            cliente = form.cleaned_data['cliente']
            print(cliente)
            resultados = Gestionar_listado.objects.filter(cliente_id__cliente_razonsocial__icontains = cliente)
        else:
            resultados = []
    else:
        form = BuscarListadoForm()
        resultados = Gestionar_listado.objects.all().order_by('-id')

    # count = Solicitudes.objects.filter(estado=1).count()
    return render(request, 'gestionar_listado.html', {'form': form, 'resultados': resultados})



def verificar_estado_gestion(gestion_id):
    # Obtiene todos los productos relacionados con la gestión
    productos_detalle = Gestionar_listado_detalle.objects.filter(gestion_id=gestion_id)

    # Verifica si todos los productos están en estado 'PG'
    if productos_detalle.exists() and all(producto.estado == 'PG' for producto in productos_detalle):
        gestion = Gestionar_listado.objects.get(id=gestion_id)
        gestion.estado = 'PG'
        gestion.save()

@login_required(login_url='login1')
def crear_listado_cliente(request):
    if request.method == "POST":
        Agregarregistro = GestionarlistadoForm(request.POST, request.FILES)
        if Agregarregistro.is_valid():
            cliente = Agregarregistro.cleaned_data.get('cliente')
            print(cliente)
            if Gestionar_listado.objects.filter(cliente=cliente, estado = 'AB').exists():
                messages.error(request, 'El cliente ya está registrado, y tiene un Saldo Pendiente Activo!.')
                return HttpResponseRedirect(reverse('crear_listado_cliente'))
            else:
                Agregarregistro.save()
                return HttpResponseRedirect(reverse('gestionar_listado'))

    else:
        form = GestionarlistadoForm()
        return render(request, 'crear_listado_cliente.html', {'form': form})

@login_required(login_url='login1')
def gestionar_listado_detalle(request,pk):
    gestion = get_object_or_404(Gestionar_listado, pk=pk)
    print(gestion)
    resultados = Gestionar_listado.objects.all()
    for gestion in resultados:
        gestion.total = gestion.calcular_total()
        gestion.pagado = gestion.calcular_pagado()
        gestion.pendiente = gestion.calcular_pendiente()
        gestion.save()
        verificar_estado_gestion(gestion.id)
    if request.method == "POST":
        Agregarproducto = GestionarlistadodetalleForm(request.POST, request.FILES)
        if Agregarproducto.is_valid():
            nuevo_registro = Agregarproducto.save(commit=False)
            nuevo_registro.gestion_id = gestion.id
            nuevo_registro.precio = nuevo_registro.precio
            nuevo_registro.total = nuevo_registro.cantidad * nuevo_registro.precio
            nuevo_registro.save()

            # Recalcular el total de todos los registros de detalle
            total_cuenta = \
            Gestionar_listado_detalle.objects.filter(gestion=gestion).aggregate(total=models.Sum('total'))['total']
            gestion.total_cuenta = total_cuenta
            gestion.save()

            return redirect('gestionar_listado_detalle', pk)

        else:
            form = GestionarlistadodetalleForm()

    else:
        form = GestionarlistadodetalleForm()
        resultados = Gestionar_listado_detalle.objects.filter(gestion = pk).order_by('fecha_registro')
        resultados_pro = Productos.objects.all()
        # Agrupar resultados por fecha
        grouped_resultados = OrderedDict()
        for resultado in resultados:
            fecha = resultado.fecha_registro
            if fecha not in grouped_resultados:
                grouped_resultados[fecha] = []
            grouped_resultados[fecha].append(resultado)

        context = {
            'grouped_resultados': dict(grouped_resultados),
            'form':form,
            'gestion':gestion,
            'resultados_pro':resultados_pro
        }

    # count = Solicitudes.objects.filter(estado=1).count()
    return render(request, 'gestionar_listado_detalle.html', context)

@login_required(login_url='login1')
def modificar_listado_detalle(request, pk):
    producto = get_object_or_404(Gestionar_listado_detalle, pk=pk)
    gestion_id = producto.gestion.pk
    resultados = Gestionar_listado.objects.all()
    for gestion in resultados:
        gestion.total = gestion.calcular_total()
        gestion.pagado = gestion.calcular_pagado()
        gestion.pendiente = gestion.calcular_pendiente()
        gestion.save()
        verificar_estado_gestion(gestion.id)
    if request.method == "POST":
        form = GestionarlistadodetalleForm(request.POST, instance=producto)
        if form.is_valid():
            producto_modificado = form.save(commit=False)
            producto_modificado.total = producto_modificado.cantidad * producto_modificado.precio
            producto_modificado.save()

            # Recalcular el total de todos los registros de detalle
            total_cuenta = \
            Gestionar_listado_detalle.objects.filter(gestion_id=gestion_id).aggregate(total=Sum('total'))['total'] or 0
            producto.gestion.total_cuenta = total_cuenta
            producto.gestion.save()
            messages.success(request, 'Producto Modificado Correctamente')
            return redirect('gestionar_listado_detalle',pk=gestion_id)  # Redireccionar a donde quieras después de modificar
    else:
        form = GestionarlistadodetalleForm(instance=producto)

        return render(request, 'modificar_listado_detalle.html',
                      {'form': form})
@login_required(login_url='login1')
def eliminar_listado(request, pk):

    if Gestionar_listado_detalle.objects.filter(estado='AB').exists():
        messages.error(request, 'El listado que desea Eliminar, tiene un saldo activo pendiente')
        return redirect('gestionar_listado')
    else:
        producto = get_object_or_404(Gestionar_listado, pk=pk)
        producto.delete()

    messages.success(request, 'Listado Eliminado con Exito')
    return redirect('gestionar_listado')

def eliminar_listado_detalle(request, pk):
    producto = get_object_or_404(Gestionar_listado_detalle, pk=pk)
    gestion_id = producto.gestion.pk
    producto.delete()
    resultados = Gestionar_listado.objects.all()
    for gestion in resultados:
        gestion.total = gestion.calcular_total()
        gestion.pagado = gestion.calcular_pagado()
        gestion.pendiente = gestion.calcular_pendiente()
        gestion.save()
        verificar_estado_gestion(gestion.id)
    messages.success(request, 'Producto Eliminado del Pedido')
    return redirect('gestionar_listado_detalle',pk=gestion_id)

@login_required(login_url='login1')
def procesar_seleccionados(request):
    if request.method == 'POST':
        factura_id = request.POST.get('factura_id')
        productos_ids = request.POST.get('productos', '').split(',')
        print(factura_id)
        print(productos_ids)
        try:
            factura = Factura.objects.get(pk=factura_id)
        except Factura.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Factura no encontrada'})

        for producto_id in productos_ids:
            if producto_id:  # Verificar que el ID no esté vacío
                try:
                    producto_detalle = Gestionar_listado_detalle.objects.get(pk=producto_id)
                    FacturaDetalle.objects.create(
                        factura=factura,
                        producto=producto_detalle.producto,
                        cantidad=producto_detalle.cantidad,
                        precio=producto_detalle.precio,
                        total=producto_detalle.total,
                        estado = 'PD',
                        pedido_id_id = producto_id
                    )
                    producto_detalle.estado = 'PG' # Asumiendo que 'PG' es el código para "pagado"
                    producto_detalle.d_factura = factura
                    producto_detalle.save()
                    recalcular_total_factura(factura)
                except Gestionar_listado_detalle.DoesNotExist:
                    return JsonResponse({'success': False, 'message': f'Producto con ID {producto_id} no encontrado'})

    # Preparar el contexto para renderizar la página
        lineas = factura.lineas.all()
        form = FacturaDetalleForm()
        resultados = Gestionar_listado_detalle.objects.filter(
            gestion__cliente__cliente_razonsocial=factura.cliente).order_by('fecha_registro')

        # Obtener el valor del IVA desde la configuración
        configuracion = Configuracion.objects.first()
        IVA_PERCENTAGE = Decimal(configuracion.iva)
        subtotal = factura.total

        # Calcular el IVA y el total
        iva = subtotal * IVA_PERCENTAGE
        total_con_iva = subtotal + iva

        subtotal = subtotal.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        iva = iva.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        total_con_iva = total_con_iva.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        grouped_resultados = OrderedDict()
        for resultado in resultados:
            stock_disponible = resultado.producto.producto_stock
            fecha = resultado.fecha_registro
            if fecha not in grouped_resultados:
                grouped_resultados[fecha] = []
            grouped_resultados[fecha].append({
                'resultado': resultado,
                'stock_disponible': stock_disponible,
            })

        context = {
            'factura': factura,
            'iva': iva,
            'total': total_con_iva,
            'form': form,
            'lineas': lineas,
            'grouped_resultados': dict(grouped_resultados),
        }

        messages.success(request, 'Productos procesados correctamente')
        return render(request, 'crear_factura_añadir_producto.html', context)
    else:
        return JsonResponse({'success': False, 'message': 'Método no permitido'})
@login_required(login_url='login1')
def gestionar_listado_imprimir_pdf(request,pk):
    gestion = get_object_or_404(Gestionar_listado, pk=pk)
    print(gestion)
    resultados = Gestionar_listado_detalle.objects.filter(gestion=pk).order_by('fecha_registro')

    # Agrupar resultados por fecha
    grouped_resultados = OrderedDict()
    for resultado in resultados:
        fecha = resultado.fecha_registro
        if fecha not in grouped_resultados:
            grouped_resultados[fecha] = []
        grouped_resultados[fecha].append(resultado)

    template_path = 'gestionar_listado_imprimir_pdf.html'

    hoy = timezone.localtime(timezone.now()).date()
    base_url = request.build_absolute_uri('/')
    # Renderiza la plantilla con los datos del registro
    context = {
        'MEDIA_URL': request.build_absolute_uri('/'),
        'grouped_resultados': dict(grouped_resultados),
        'gestion': gestion,
        'hoy': hoy,
    }
    template = get_template(template_path)
    rendered_html = template.render(context)

    # Crea un buffer en memoria para guardar el PDF
    response_buffer = BytesIO()
    pdf_status = pisa.CreatePDF(BytesIO(rendered_html.encode("utf-8")), dest=response_buffer, encoding='utf-8')

    # Verifica si hubo errores al generar el PDF
    if pdf_status.err:
        return HttpResponse('Hubo un error al generar el PDF', status=500)

    # Devuelve el PDF como una respuesta HTTP para descargar o mostrar en el navegador
    response = HttpResponse(response_buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=Reporte_listado_estado_{pk}.pdf'
    return response
    # rendered_html = render(request, template_path, context)
    # # Genera el PDF con WeasyPrint
    # pdf = HTML(string=rendered_html.content, base_url=base_url).write_pdf()
    #
    # # Devuelve el PDF como una respuesta HTTP para descargar
    # response = HttpResponse(pdf, content_type='application/pdf')
    # response['Content-Disposition'] = f'inline; filename=Reporte_listado_estado_{pk}.pdf'
    # return response