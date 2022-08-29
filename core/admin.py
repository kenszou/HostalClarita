from django.contrib import admin
from .models import Bodega, Cliente, Cocina, Comanda, Departamento, Empleado,\
     EstadoHabitacion, Factura, HostalClarita, Huesped, OrdenCompra, Pedido, Producto \
     ,Proveedor, TipoHabitacion, Minuta, Usuario, TipoUsuario, reserva,Factura_hostal \
     ,Recepcion_Pedidoh
# Register your models here para hacer un CRUD en el area administrador.

admin.site.register(Bodega)
admin.site.register(Cliente)
admin.site.register(Cocina)
admin.site.register(Comanda)
admin.site.register(Departamento)
admin.site.register(Empleado)
admin.site.register(EstadoHabitacion)
admin.site.register(Factura)
admin.site.register(HostalClarita)
admin.site.register(Huesped)
admin.site.register(Minuta)
admin.site.register(OrdenCompra)
admin.site.register(Pedido)
admin.site.register(Producto)
admin.site.register(Proveedor)
admin.site.register(TipoHabitacion)
admin.site.register(TipoUsuario)
admin.site.register(Usuario)
admin.site.register(reserva)
admin.site.register(Factura_hostal)
admin.site.register(Recepcion_Pedidoh)
