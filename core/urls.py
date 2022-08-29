from django.urls import path
from django.urls.conf import include
from .views import *
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', home, name="home"),
    path('listado-usuario', listado_usuario, name="listado_usuario"),
    path('nuevo-usuario', nuevo_usuario, name="nuevo_usuario"),
    path('modificar/<id_usuario>/', modificar_usuario, name="modificar_usuario"),
    path('eliminar/<id_usuario>/', eliminar_usuario, name="eliminar_usuario"),
    path('registro', registro, name="registro"),
    path('empresa', nueva_empresa, name="empresa"),
    path('huesped', huesped_registro, name="huesped"),
    path('recepcion-pedido', recepcion_pedido, name="recepcion_pedido"),
    path('registro-pedido', registro_pedido, name="registro_pedido"),
    path('orden-compra', orden_compra, name="orden_compra"),
    path('orden-pedido', orden_pedido, name="orden_pedido"),
    path('factura-registro', registro_factura, name="factura"),
    path('registro-habitacion', registro_habitacion, name="registro_habitacion"),
    path('registro-proveedor', registro_proveedor, name="registro_proveedor"),
    path('reserva-huesped', reserva_huesped, name="reserva_huesped"),
    path('menu-admin', menu_admin, name="menu_admin"),
    path('buscar_factura', buscar_factura, name="buscar_factura"),
    path('menu_reporte', menu_reporte, name="menu_reporte"),
    path('menu_manual', menu_manual, name="menu_manual"),

    path('manual_admin', manual_admin, name="manual_admin"),
    path('manual_cliente', manual_cliente, name="manual_cliente"),
    path('manual_empleado', manual_empleado, name="manual_empleado"),
    path('manual_proveedor', manual_proveedor, name="manual_proveedor"),
    path('manual_sistema', manual_sistema, name="manual_sistema"),
    
    path('comedor', comedor , name="comedor"),
    path('reporte', reporte.as_view() , name="reporte"),
    path('reporte_reserva', reporte_reserva.as_view() , name="reporte_reserva"),
    path('reporte_proveedor', reporte_proveedor.as_view() , name="reporte_proveedor"),
    path('reporte_factura', reporte_factura.as_view() , name="reporte_factura"),
    path('reporte_pedido', reporte_pedido.as_view() , name="reporte_pedido"),
  
    
  
    
    
]