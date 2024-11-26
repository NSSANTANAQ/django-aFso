# Generated by Django 5.0.6 on 2024-11-26 18:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Configuracion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iva', models.DecimalField(decimal_places=2, default=0.15, max_digits=5)),
                ('porcentaje_credito', models.DecimalField(decimal_places=2, default=0.5, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Clientes',
            fields=[
                ('cliente_id', models.AutoField(primary_key=True, serialize=False)),
                ('cliente_ruc', models.CharField(max_length=13)),
                ('cliente_razonsocial', models.CharField(max_length=255)),
                ('cliente_direccion', models.CharField(max_length=255)),
                ('telefono', models.CharField(max_length=20)),
                ('correo', models.CharField(max_length=150)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('usuario_creacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clientescreado_por', to=settings.AUTH_USER_MODEL)),
                ('usuario_modificacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clientesmodificado_por', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'clientes',
                'verbose_name_plural': 'clientes',
                'db_table': 'clientes',
            },
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(blank=True, max_length=20, unique=True)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('tipo_pago', models.CharField(choices=[('EFECTIVO', 'EFECTIVO'), ('CREDITO', 'CREDITO')], default='EFECTIVO', max_length=10)),
                ('estado', models.CharField(choices=[('AB', 'Abierta'), ('CE', 'Cerrada'), ('DV', 'Devuelta')], default='AB', max_length=2)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.clientes')),
            ],
        ),
        migrations.CreateModel(
            name='Gestionar_listado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio', models.DateField()),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('pendiente', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('pagado', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('estado', models.CharField(default='AB', max_length=2)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.clientes')),
            ],
        ),
        migrations.CreateModel(
            name='Presentacion',
            fields=[
                ('presentacion_id', models.AutoField(primary_key=True, serialize=False)),
                ('presentacion_detalle', models.CharField(max_length=150)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('usuario_creacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='presentacioncreado_por', to=settings.AUTH_USER_MODEL)),
                ('usuario_modificacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='presentacionmodificado_por', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'presentacion',
                'verbose_name_plural': 'presentacion',
                'db_table': 'presentacion',
            },
        ),
        migrations.CreateModel(
            name='Movimientoproductos',
            fields=[
                ('mov_producto_id', models.AutoField(primary_key=True, serialize=False)),
                ('mov_producto_tipo', models.CharField(max_length=200)),
                ('mov_producto_nom', models.CharField(max_length=200)),
                ('mov_producto_fechaingreso', models.DateField()),
                ('mov_producto_cantidad', models.PositiveIntegerField()),
                ('mov_producto_precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('mov_producto_observacion', models.CharField(max_length=300)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('usuario_creacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movimientoproductoscreado_por', to=settings.AUTH_USER_MODEL)),
                ('usuario_modificacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='movimientoproductosmodificado_por', to=settings.AUTH_USER_MODEL)),
                ('mov_producto_presentacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.presentacion')),
            ],
            options={
                'verbose_name': 'Movimientoproductos',
                'verbose_name_plural': 'Movimientoproductos',
                'db_table': 'Movimientoproductos',
            },
        ),
        migrations.CreateModel(
            name='Productos',
            fields=[
                ('producto_id', models.AutoField(primary_key=True, serialize=False)),
                ('producto_nom', models.CharField(max_length=200)),
                ('producto_fechaingreso', models.DateField()),
                ('producto_stock', models.PositiveIntegerField()),
                ('producto_precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('producto_presentacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventario.presentacion')),
                ('usuario_creacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productocreado_por', to=settings.AUTH_USER_MODEL)),
                ('usuario_modificacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productomodificado_por', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Productos',
                'verbose_name_plural': 'Productos',
                'db_table': 'Productos',
            },
        ),
        migrations.CreateModel(
            name='Gestionar_listado_detalle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_registro', models.DateField()),
                ('cantidad', models.PositiveIntegerField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('estado', models.CharField(default='AB', max_length=2)),
                ('d_factura', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventario.factura')),
                ('gestion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gestion_listado', to='inventario.gestionar_listado')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='producto_listado', to='inventario.productos')),
            ],
        ),
        migrations.CreateModel(
            name='FacturaDetalle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('estado', models.CharField(default='PD', max_length=2)),
                ('factura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lineas', to='inventario.factura')),
                ('pedido_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inventario.gestionar_listado_detalle')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='producto', to='inventario.productos')),
            ],
        ),
    ]
