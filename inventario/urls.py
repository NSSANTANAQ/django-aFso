from django.urls import path, include
from . import views
from .views import ProductosAutocomplete,ClientesAutocomplete


urlpatterns = [
    path('menu_sistemas/', views.menu_sistemas, name="menu_sistemas"),
    path('consulta_producto_stock/', views.consulta_producto_stock, name="consulta_producto_stock"),
    path('crear_producto_stock/', views.crear_producto_stock, name="crear_producto_stock"),
    path('crear_presentacion/', views.crear_presentacion, name="crear_presentacion"),
    path('modificar_presentacion/', views.modificar_presentacion, name="modificar_presentacion"),
    path('obtener_datos_actualizados/', views.obtener_datos_actualizados, name="obtener_datos_actualizados"),
    path('consulta_producto_movimiento/', views.consulta_producto_movimiento, name="consulta_producto_movimiento"),
    path('crear_producto_movimiento/', views.crear_producto_movimiento, name="crear_producto_movimiento"),
    path('modificar_producto_movimiento/<int:pk>/', views.modificar_producto_movimiento, name="modificar_producto_movimiento"),
    path('buscar-productos/', views.buscar_productos, name='buscar_productos'),
    path('buscar-productos_2/', views.buscar_productos_2, name='buscar_productos_2'),
    path('buscar_clientes/', views.buscar_clientes, name='buscar_clientes'),

    path('consulta_factura/', views.consulta_factura, name='consulta_factura'),
    path('imprimir_factura/<int:id>/', views.imprimir_factura, name='imprimir_factura'),
    path('crear_factura_producto/<int:factura_id>/', views.crear_factura_producto, name='crear_factura_producto'),
    path('crear-factura/', views.crear_factura, name='crear_factura'),
    path('actualizar_tipo_pago/<int:factura_id>/', views.actualizar_tipo_pago, name='actualizar_tipo_pago'),
    path('finalizar_factura/<int:factura_id>/', views.finalizar_factura, name='finalizar_factura'),
    path('eliminar_factura/<int:factura_id>/', views.eliminar_factura, name='eliminar_factura'),
    path('eliminar_producto_factura/<int:producto_id>/', views.eliminar_producto_factura, name='eliminar_producto_factura'),

    path('consulta_cliente/', views.consulta_cliente, name='consulta_cliente'),
    path('crear_cliente/', views.crear_cliente, name='crear_cliente'),
    path('modificar_clientes/<int:pk>/', views.modificar_clientes, name='modificar_clientes'),
    path('eliminar_clientes/<int:pk>/', views.eliminar_clientes, name='eliminar_clientes'),
    path('configuracion/', views.configuracion_view, name='configuracion_view'),

    path('productos-autocomplete/', ProductosAutocomplete.as_view(), name='productos-autocomplete'),
    path('clientes-autocomplete/', ClientesAutocomplete.as_view(), name='clientes-autocomplete'),
    path('reportes_generales/', views.reportes_generales, name='reportes_generales'),

    path('pantalla-carga/<int:id>/', views.pantalla_carga, name='pantalla_carga'),

    path('modificar_productos/<int:pk>/', views.modificar_productos, name='modificar_productos'),
    path('gestionar_perfil/', views.gestionar_perfil, name='gestionar_perfil'),
    path('cambiar_password/', views.cambiar_password, name='cambiar_password'),

    path('gestionar_listado/', views.gestionar_listado, name='gestionar_listado'),
    path('crear_listado_cliente/', views.crear_listado_cliente, name='crear_listado_cliente'),
    path('gestionar_listado_detalle/<int:pk>', views.gestionar_listado_detalle, name='gestionar_listado_detalle'),
    path('modificar_listado_detalle/<int:pk>', views.modificar_listado_detalle, name='modificar_listado_detalle'),
    path('eliminar_listado/<int:pk>', views.eliminar_listado, name='eliminar_listado'),
    path('eliminar_listado_detalle/<int:pk>', views.eliminar_listado_detalle, name='eliminar_listado_detalle'),
    path('gestionar_listado_imprimir_pdf/<int:pk>', views.gestionar_listado_imprimir_pdf, name='gestionar_listado_imprimir_pdf'),
    path('procesar_seleccionados/', views.procesar_seleccionados, name='procesar_seleccionados'),


    path('obtener_precio_producto_presentacion/', views.obtener_precio_producto_presentacion, name='obtener_precio_producto_presentacion'),

]