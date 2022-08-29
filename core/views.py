import django
from django.contrib.auth.forms import PasswordResetForm
from django.db.models.query import QuerySet
from django.forms.widgets import DateTimeBaseInput
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import TemplateView
from .models import Factura_hostal, Proveedor, TipoHabitacion, Usuario, Pedido, comedor, reserva, Recepcion_pedido
from .forms import UsuarioForm, CustomUserCreationForm, ClienteForm, HuespedForm, OrdenPedidoForm, HuespedForm, FacturaForm, OrdenCompraForm,RecepcionPedidoForm
from django.contrib import messages #permite enviar mensajes
from django.core.paginator import Paginator #para dividir las paginas con los usuarios agregados
from django.http import Http404, request, HttpResponse
from django.contrib.auth import authenticate, login #autentica usuario
from django.contrib.auth.decorators import login_required, permission_required
from django.db import connection #trae la coneccion de la base de datos
from django.views.generic import View
import cx_Oracle
from django.db.models import Q

""" PARA IMPRIMIR PDF """
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import context, pisa
from django.contrib.staticfiles import finders




#crear vista
def home(request):#la pagina de inicio
    return render(request,'core/home.html')

def buscar_factura(request):
    busqueda = request.GET.get("buscar")
    listado = Factura_hostal.objects.all()
    if busqueda:
        listado = Factura_hostal.objects.filter(
            #revisa cada uno de los campos del models
            Q(rut_empresa__icontains = busqueda)             
        ).distinct()
    
  
    return render(request,'core/buscar_factura.html',{'factura':listado})



@permission_required('core.view_cliente')
def listado_usuario(request):
    usuario = Usuario.objects.all()
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(usuario, 5)
        usuario = paginator.page(page)
    except:
        raise Http404

    data ={
        'entity':usuario,
        'paginator':paginator
    }
    return render(request, 'core/listado_usuarios.html', data)
    
@permission_required('core.add_usuario')
def nuevo_usuario(request):
    data = {
        'form':UsuarioForm()
    }

    if request.method == 'POST':
        formulario = UsuarioForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Usuario Agregado Correctamente")
            

    return render(request, 'core/nuevo_usuario.html', data)

@permission_required('core.change_usuario')
def modificar_usuario(request, id_usuario):
    usuario = get_object_or_404(Usuario, id_usuario=id_usuario)
    data = {
        'form': UsuarioForm(instance=usuario)
    }
    if request.method == 'POST':
        formulario = UsuarioForm(data=request.POST, instance=usuario, files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Modificado Correctamente")#envia el mensaje
            return redirect(to="listado_usuario")
        data["form"] = formulario    
    return render(request, 'core/modificar.html', data)

@permission_required('core.delete_usuario')
def eliminar_usuario(request, id_usuario):

    usuario = get_object_or_404(Usuario, id_usuario=id_usuario)
    usuario.delete()
    messages.success(request, "Eliminado Correctamente")
    return redirect(to="listado_usuario")

def registro(request):
    data = {
        'form': CustomUserCreationForm()
    }

    if request.method == 'POST':
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)
            messages.success(request, "Cliente registrado correctamente")
            return redirect(to='/')
        data["form"] = formulario 

    return render(request,'registration/registro.html', data)

@permission_required('core.add_cliente')
def nueva_empresa(request):
    data = {
        'form': ClienteForm()
    }

    if request.method == 'POST':
        formulario = ClienteForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Empresa registrada")
            return redirect(to='home')
    return render(request, 'core/empresa.html', data)

@permission_required('core.add_cliente')
def huesped_registro(request):
    data = {
        'form': HuespedForm()
    }
    if request.method == 'POST':
        formulario = HuespedForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Huesped registrado")
            return redirect(to='menu_admin')  
        data["form"] = formulario     
    return render(request, 'core/huesped.html', data)

@permission_required('core.add_cliente')
def recepcion_pedido(request):
    return render(request, 'core/recepcion_pedido.html')

@permission_required('core.view_pedido')
def orden_pedido(request):
    pedido = Pedido.objects.all()
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(pedido, 5)
        pedido = paginator.page(page)
    except:
        raise Http404

    data ={
        'entity':pedido,
        'paginator':paginator
    }

    return render(request, 'core/recepcion_pedido.html', data)

@permission_required('core.view_pedido')
def recepcion_pedido(request):
    pedido = Pedido.objects.all()
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(pedido, 5)
        pedido = paginator.page(page)
    except:
        raise Http404

    data ={
        'entity':pedido,
        'paginator':paginator,
        'registro_proveedor':listar_proveedor()
    }
    return render(request, 'core/recepcion_pedido.html', data)

@permission_required('core.add_cliente')
def orden_compra(request):
    data = {
        'form': OrdenCompraForm()
    }
    if request.method == 'POST':
        formulario = OrdenCompraForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Orden registrada")
            return redirect(to='orden_pedido')  
        data["form"] = formulario     
    return render(request, 'core/orden_compra.html', data)

@permission_required('core.add_cliente')
def registro_factura(request):
    data = {
        'empresa':listado_empresa()
    }
    if request.method == 'POST': 
        FECHA_FACTURA = request.POST.get('fecha_factura') 
        RUT_EMPRESA = request.POST.get('rut empresa')
        DETALLE_FACTURA = request.POST.get('detalle')
        VALOR_FACTURA = request.POST.get('valor') 
        VALOR_IVA = request.POST.get('valor_iva')
        salida = registrar_factura(FECHA_FACTURA,RUT_EMPRESA,DETALLE_FACTURA,VALOR_FACTURA,VALOR_IVA)
        if salida == 1:
            messages.success(request, "agregado correctamente")
            data['mensaje'] = 'agregado correctamente'
            data['empresa'] = listado_empresa()
        else:
            data['mensaje'] = 'no se ha guardado'
    return render(request, 'core/factura.html',data)

def Agregar_pedido(request):
    data = {
        'form':RecepcionPedidoForm()
    }

    if request.method == 'POST':
        formulario = RecepcionPedidoForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, "Pedido Agregado Correctamente")
            

    return render(request, 'core/recepcion_pedido.html', data)

def registro_pedido(request):
    data = {
        'empresa':listado_empresa()        
    }
    if request.method == 'POST': 
        COD_PROVEEDOR = request.POST.get('proveedor') 
        NOM_PRODUCTO = request.POST.get('nombre')
        CATEGORIA_PRODUCTO = request.POST.get('categoria')
        FECHA_VENCIMIENTO = request.POST.get('vencimiento')
        NUMERO_SECUENCIAL = request.POST.get('secuencial') 
        SKU = request.POST.get('sku')        
        salida = registrar_pedido(COD_PROVEEDOR,NOM_PRODUCTO,CATEGORIA_PRODUCTO,FECHA_VENCIMIENTO,NUMERO_SECUENCIAL,SKU)
        if salida == 1:
            messages.success(request, "agregado correctamente")
            data['mensaje'] = 'agregado correctamente'
            data['empresa'] = listado_empresa()
        else:
            data['mensaje'] = 'no se ha guardado'
    return render(request, 'core/registro_pedido.html',data)

def registrar_pedido(COD_PROVEEDOR,NOM_PRODUCTO,CATEGORIA_PRODUCTO,FECHA_VENCIMIENTO,NUMERO_SECUENCIAL,SKU):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_PEDIDO',[COD_PROVEEDOR,NOM_PRODUCTO,CATEGORIA_PRODUCTO,FECHA_VENCIMIENTO,NUMERO_SECUENCIAL,SKU,salida])     
    return salida.getvalue()

def registro_habitacion(request):
    tiphab = TipoHabitacion.objects.all()
    page = request.GET.get('page', 1)

    try:
        paginator = Paginator(tiphab, 6)
        tiphab = paginator.page(page)
    except:
        raise Http404

    data ={
        'entity':tiphab,
        'paginator':paginator
    }
    
    return render(request,'core/registro_habitacion.html',data)

def registro_proveedor(request):
    data = {
        'registro_proveedor':listar_proveedor()
    }

    if request.method == 'POST':
        rut_proveedor = request.POST.get('rut') 
        nom_proveedor = request.POST.get('nombre') 
        rubro_proveedor = request.POST.get('rubro') 
        tel_proveedor = request.POST.get('telefono') 
        salida = agregar_proveedor(rut_proveedor,nom_proveedor,rubro_proveedor,tel_proveedor)
        if salida == 1:
            messages.success(request, "agregado correctamente")
            data['mensaje'] = 'agregado correctamente'
            data['registro_proveedor'] = listar_proveedor()
        else:
            data['mensaje'] = 'no se ha guardado'
    return render(request, 'core/registro_proveedor.html',data)    

def listar_proveedor():   
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_PROVEEDOR", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def agregar_proveedor(rut_proveedor, nom_proveedor, rubro_proveedor, tel_proveedor):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_PROVEEDOR',[rut_proveedor,nom_proveedor,rubro_proveedor,tel_proveedor,salida])     
    return salida.getvalue()

def registrar_factura(FECHA_FACTURA,RUT_EMPRESA,DETALLE_FACTURA,VALOR_FACTURA,VALOR_IVA):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_REGISTRAR_FACTURA',[FECHA_FACTURA,RUT_EMPRESA,DETALLE_FACTURA,VALOR_FACTURA,VALOR_IVA,salida])     
    return salida.getvalue()

def reserva_huesped(request):
    data = {
        'empresa':listado_empresa(),
        'huesped':listado_huesped(),
        'habitacion':listado_habitacion(),
        'listado_huesped':listado_huespedes()
    }
    if request.method == 'POST':
        rut_empresa = request.POST.get('rut empresa') 
        rut_huesped = request.POST.get('rut huesped') 
        id_tipo_habitacion = request.POST.get('id tipo habitacion') 
        check_in = request.POST.get('check_in') 
        check_out = request.POST.get('check_out')
        salida = registrar_reserva(rut_empresa,rut_huesped,id_tipo_habitacion,check_in,check_out)
        if salida == 1:
            messages.success(request, "agregado correctamente")
            data['mensaje'] = 'agregado correctamente'
            data['listado_huesped'] = listado_huespedes()
        else:
            data['mensaje'] = 'no se ha guardado'
    return render(request, 'core/reserva_huesped.html',data)  

def listado_empresa():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_RUTEMPRESA", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def listado_comedor():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_COMEDOR", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def listado_huesped():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_RUTHUESPED", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def listado_habitacion():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_IDHABITACION", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def listado_huespedes():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_RESERVA", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def registrar_reserva(rut_empresa,rut_huesped,id_tipo_habitacion,check_in,check_out):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_GENERAR_RESERVA',[rut_empresa,rut_huesped,id_tipo_habitacion,check_in,check_out,salida])     
    return salida.getvalue()

def menu_admin(request):
    return render(request,'core/menuadmin.html')

def menu_reporte(request):
    return render(request,'core/menureporte.html')

def menu_manual(request):
    return render(request,'core/menumanual.html')
def manual_admin(request):
    return render(request,'manual/admi.html')
def manual_cliente(request):
    return render(request,'manual/cliente.html')
def manual_empleado(request):
    return render(request,'manual/empleado.html')
def manual_proveedor(request):
    return render(request,'manual/proveedor.html')
def manual_sistema(request):
    return render(request,'manual/sistema.html')

def comedor(request):
    data = {
        'comedor':listar_comedor()
    }
    if request.method == 'POST':
        nombre_plato = request.POST.get('nombre') 
        detalle = request.POST.get('detalle') 
        valor_plato = request.POST.get('valor') 
        tipo_servicio = request.POST.get('servicio') 
        salida = registrar_comedor(nombre_plato,detalle,valor_plato,tipo_servicio)
        if salida == 1:
            messages.success(request, "agregado correctamente")
            data['mensaje'] = 'agregado correctamente'
            data['comedor'] = listar_comedor()
        else:
            data['mensaje'] = 'no se ha guardado'

    return render(request,'core/comedor.html',data)

def listar_comedor():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur = django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_COMEDOR", [out_cur])

    lista = []
    for fila in out_cur:
        lista.append(fila)
    return lista

def registrar_comedor(nombre_plato,detalle,valor_plato,tipo_servicio):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_COMEDOR',[nombre_plato,detalle,valor_plato,tipo_servicio,salida])     
    return salida.getvalue()



class reporte(View):
    def get(self, request, *args, **kwargs):
        template = get_template('reportes/reporte_usuario.html')
        context = {
            'usuario': Usuario.objects.all()
        }
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        """ response['Content-Disposition'] = 'attachment; filename="report.pdf"' """
        pisa_status = pisa.CreatePDF(
            html, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')

        return response
        
class reporte_reserva(View):
    def get(self, request, *args, **kwargs):
        template = get_template('reportes/reporte_reserva.html')
        context = {
            'Reserva': reserva.objects.all()
        }
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        """ response['Content-Disposition'] = 'attachment; filename="report.pdf"' """
        pisa_status = pisa.CreatePDF(
            html, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')

        return response

class reporte_proveedor(View):
    def get(self, request, *args, **kwargs):
        template = get_template('reportes/reporte_proveedor.html')
        context = {
            'proveedor': Proveedor.objects.all()
        }
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        """ response['Content-Disposition'] = 'attachment; filename="report.pdf"' """
        pisa_status = pisa.CreatePDF(
            html, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')

        return response

class reporte_factura(View):
    def get(self, request, *args, **kwargs):
        template = get_template('reportes/reporte_factura.html')
        context = {
            'factura': Factura_hostal.objects.all()
        }
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        """ response['Content-Disposition'] = 'attachment; filename="report.pdf"' """
        pisa_status = pisa.CreatePDF(
            html, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')

        return response

class reporte_pedido(View):
    def get(self, request, *args, **kwargs):
        template = get_template('reportes/reporte_pedido.html')
        context = {
            'entity': Pedido.objects.all()
        }
        html = template.render(context)
        response = HttpResponse(content_type='application/pdf')
        """ response['Content-Disposition'] = 'attachment; filename="report.pdf"' """
        pisa_status = pisa.CreatePDF(
            html, dest=response)
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')

        return response
        
