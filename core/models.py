from django.db import models
from django.db.models.base import Model
#crea la base de datos

class Bodega(models.Model):
    id_bodega = models.IntegerField(primary_key=True)
    cant_producto = models.IntegerField()
    nom_producto = models.CharField(max_length=50)
    fecha_recepcionada = models.DateField()
    fecha_vencimiento = models.DateField()

    class Meta:
        managed = True
        db_table = 'bodega'

class HostalClarita(models.Model):
    rut_hostal = models.IntegerField(primary_key=True)
    direccion = models.CharField(max_length=50)
    tel_hostal = models.CharField(max_length=12)

    class Meta:
        managed = True
        db_table = 'hostal_clarita'


class Cliente(models.Model):
    rut_empresa = models.CharField(max_length=12, primary_key=True)
    nom_empresa = models.CharField(max_length=20)
    tel_empresa = models.CharField(max_length=15)
    direc_empresa = models.CharField(max_length=50)
    hostal_clarita_rut_hostal = models.ForeignKey(HostalClarita, on_delete=models.PROTECT)

    class Meta:
        managed = True
        db_table = 'cliente'
        unique_together = (('rut_empresa', 'hostal_clarita_rut_hostal'),)

class Departamento(models.Model):
    id_departamento = models.IntegerField(primary_key=True)
    nom_departamento = models.CharField(max_length=20)

    class Meta:
        managed = True
        db_table = 'departamento'


class Cocina(models.Model):
    id_cocina = models.IntegerField(primary_key=True)
    departamento_id_departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT)

    class Meta:
        managed = True
        db_table = 'cocina'
        unique_together = (('id_cocina', 'departamento_id_departamento'),)

class Minuta(models.Model):
    id_minuta = models.IntegerField(primary_key=True)
    nom_minuta = models.CharField(max_length=20)
    valor_minuta = models.BigIntegerField()

    class Meta:
        managed = True
        db_table = 'minuta'

class Huesped(models.Model):
    rut_huesped = models.CharField(max_length=12 ,primary_key=True)
    nom_huesped = models.CharField(max_length=15)
    apellido_huesped = models.CharField(max_length=15)
    tel_huesped = models.CharField(max_length=12)
    correo_huesped = models.CharField(max_length=20)

    class Meta:
        managed = True
        db_table = 'huesped'



class Comanda(models.Model):
    id_comanda = models.IntegerField(primary_key=True)
    descripcion_comanda = models.CharField(max_length=50)
    cocina_id_cocina = models.ForeignKey(Cocina, on_delete=models.PROTECT)
    cocina_departamento_id_departamento = models.ForeignKey(Cocina,on_delete=models.PROTECT, related_name='cocina_depa')
    minuta_id_minuta = models.ForeignKey(Minuta, on_delete=models.PROTECT)
    huesped_rut_huesped = models.ForeignKey(Huesped, on_delete=models.PROTECT)

    class Meta:
        managed = True
        db_table = 'comanda'
        unique_together = (('id_comanda', 'cocina_id_cocina', 'cocina_departamento_id_departamento', 'minuta_id_minuta', 'huesped_rut_huesped'),)

class Pedido(models.Model):
    id_pedido = models.AutoField(primary_key=True)
    cantidad = models.IntegerField()
    fecha_emision_pedido = models.DateField()
    fecha_recepcion = models.DateField()
    estado_pedido = models.CharField(max_length=20)
    nombre_producto = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'pedido'

class Empleado(models.Model):
    rut_empleado = models.CharField(max_length=12 ,primary_key=True)
    nombre = models.CharField(max_length=20)
    apellido_materno = models.CharField(max_length=20)
    apellido_paterno = models.CharField(max_length=20)
    hostal_clarita_rut_hostal = models.ForeignKey(HostalClarita, on_delete=models.PROTECT)
    departamento_id_departamento = models.ForeignKey(Departamento, on_delete=models.PROTECT)
    pedido_id_pedido = models.ForeignKey(Pedido, on_delete=models.PROTECT)

    class Meta:
        managed = True
        db_table = 'empleado'
        unique_together = (('rut_empleado', 'hostal_clarita_rut_hostal', 'departamento_id_departamento', 'pedido_id_pedido'),)

class TipoHabitacion(models.Model):
    id_tipo_habitacion = models.IntegerField(primary_key=True)
    detalle_habitacion = models.CharField(max_length=100)
    valor_habitacion = models.IntegerField()
    tipo_hab = models.CharField(max_length=50)
    hostal_clarita_rut_hostal = models.ForeignKey(HostalClarita, on_delete=models.PROTECT)

    class Meta:
        managed = True
        db_table = 'tipo_habitacion'
        unique_together = (('id_tipo_habitacion', 'hostal_clarita_rut_hostal'),)

class EstadoHabitacion(models.Model):
    id_habitacion = models.IntegerField(primary_key=True)
    descripcion_estado = models.CharField(max_length=20)
    tipo_habitacion_id_tipo_habitacion = models.ForeignKey(TipoHabitacion, on_delete=models.PROTECT, related_name='tipo_habitacion')
    tipo_habitacion_hostal_clarita_rut_hostal = models.ForeignKey(TipoHabitacion, on_delete=models.PROTECT, related_name='habitacion_hostal')

    class Meta:
        managed = True
        db_table = 'estado_habitacion'
        unique_together = (('id_habitacion', 'tipo_habitacion_id_tipo_habitacion', 'tipo_habitacion_hostal_clarita_rut_hostal'),)


class Factura(models.Model):
    cod_factura = models.AutoField(primary_key=True)
    detalle_factura = models.CharField(max_length=50)
    fecha_factura = models.DateField()
    valor_factura = models.IntegerField()
    valor_iva = models.FloatField()
    cliente_rut_empresa = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    cliente_hostal_clarita_rut_hostal = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='cliente_clarita')

    class Meta:
        managed = True
        db_table = 'factura'
        unique_together = (('cod_factura', 'cliente_rut_empresa', 'cliente_hostal_clarita_rut_hostal'),)


class OrdenCompra(models.Model):
    id_orden = models.AutoField(primary_key=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    descripcion_compra = models.CharField(max_length=50)
    valor_compra = models.IntegerField()
    huesped_rut_huesped = models.ForeignKey(Huesped, on_delete=models.PROTECT)
    factura_cod_factura = models.ForeignKey(Factura,on_delete=models.PROTECT)
    factura_cliente_rut_empresa = models.ForeignKey(Factura, on_delete=models.PROTECT, related_name='factura_empresa')
    factura_cliente_hostal_clarita_rut_hostal = models.ForeignKey(Factura, on_delete=models.PROTECT, related_name='factura_hostal')

    class Meta:
        managed = True
        db_table = 'orden_compra'
        unique_together = (('id_orden', 'huesped_rut_huesped', 'factura_cod_factura', 'factura_cliente_rut_empresa', 'factura_cliente_hostal_clarita_rut_hostal'),)

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nom_producto = models.CharField(max_length=20)
    marca = models.CharField(max_length=20)
    valor = models.BigIntegerField()
    pedido_id_pedido = models.ForeignKey(Pedido, on_delete=models.PROTECT)
    bodega_id_bodega = models.ForeignKey(Bodega, on_delete=models.PROTECT)

    class Meta:
        managed = True
        db_table = 'producto'
        unique_together = (('id_producto', 'pedido_id_pedido', 'bodega_id_bodega'),)


class Proveedor(models.Model):
    rut_proveedor = models.CharField(max_length=12, primary_key=True)
    nom_proveedor = models.CharField(max_length=50)
    rubro_proveedor = models.CharField(max_length=50)
    tel_proveedor = models.CharField(max_length=12)
    class Meta:
        managed = True
        db_table = 'proveedor'
        


class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nom_usuario = models.CharField(max_length=20)
    clave = models.CharField(max_length=12)
    tipo_usuario = models.CharField(max_length=15)

    class Meta:
        managed = True
        db_table = 'usuario'

class TipoUsuario(models.Model):
    id_tipo = models.AutoField(primary_key=True)
    tipo_usuario = models.CharField(max_length=15)

    class Meta:
        managed = True
        db_table = 'tipo_usuario'

class reserva(models.Model):
    id_reserva = models.AutoField(primary_key=True)
    rut_empresa = models.CharField(max_length=12)
    rut_huesped = models.CharField(max_length=12)
    id_tipo_habitacion = models.IntegerField()
    check_in = models.DateField()
    check_out = models.DateField()

    class Meta:
        managed = True
        db_table = 'reserva'

class comedor(models.Model):
    id_plato = models.AutoField(primary_key=True)
    nombre_plato = models.CharField(max_length=50)
    detalle = models.CharField(max_length=100)
    valor_plato = models.IntegerField()
    tipo_servicio = models.CharField(max_length=50)

    class Meta:
        managed = True
        db_table = 'comedor'

class Factura_hostal(models.Model):
    cod_factura = models.AutoField(primary_key=True)
    fecha_factura = models.DateField()
    rut_empresa = models.CharField(max_length=100)
    detalle_factura = models.CharField(max_length=800)
    valor_factura = models.IntegerField()
    valor_iva = models.IntegerField()

    class Meta:
        managed = True
        db_table = 'factura_hostal'

class Recepcion_pedido(models.Model):
    cod_proveedor = models.IntegerField(primary_key=True)
    nom_producto = models.CharField(max_length=100)
    categoria_producto = models.IntegerField()
    fecha_vencimiento = models.IntegerField()
    numero_secuencial = models.IntegerField()
    sku = models.IntegerField()
    class Meta:
        managed = True
        db_table = 'recepcion_pedido'

class Recepcion_Pedidoh(models.Model):
    cod_pedido = models.AutoField(primary_key=True)
    cod_proveedor = models.IntegerField()
    nom_producto = models.CharField(max_length=100)
    categoria_producto = models.IntegerField()
    fecha_vencimiento = models.IntegerField()
    numero_secuencial = models.IntegerField()
    sku = models.BigIntegerField()
    class Meta:
        managed = True
        db_table = 'recepcion_pedidoh'
