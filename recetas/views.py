# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.utils import timezone
from django.views.generic import TemplateView
from django.core import serializers
from django.db import connection
import json
# Create your views here.
from .models import Receta, DetalleReceta
from clientes.models import Cliente
from medicamentos.models import Medicamentos
from django.db import transaction
from django.contrib import messages
from django.views.generic import ListView
from django.template import RequestContext as ctx
from datetime import datetime

#reporte pdf
from django.http import HttpResponseRedirect
from datetime import *
import xhtml2pdf.pisa as pisa
from django import http
from django.template.loader import get_template
from django.template import Context
from io import BytesIO
from xhtml2pdf import pisa
import cgi

from .forms import RangoForm


# Create your views here.
@login_required
@transaction.atomic
def recetaCrear(request):
    form = None
    if request.method == 'POST':
        sid = transaction.savepoint()
        try:
            proceso = json.loads(request.POST.get('proceso'))
            print
            proceso
            if 'serie' not in proceso:
                msg = 'Ingrese serie'
                raise Exception(msg)

            if 'numero' not in proceso:
                msg = 'Ingrese numero'
                raise Exception(msg)

            if 'clienProv' not in proceso:
                msg = 'El cliente no ha sido seleccionado'
                raise Exception(msg)

            if len(proceso['medicamento']) <= 0:
                msg = 'No se ha seleccionado ningun medicamento'
                raise Exception(msg)

            total = 0

            for k in proceso['medicamento']:
                medicamento = Medicamentos.objects.get(id=k['serial'])
                subTotal = (medicamento.precio_venta) * int(k['cantidad'])
                total += subTotal

            crearReceta = Receta(
                serie=proceso['serie'],
                numero=proceso['numero'],

                cliente=Cliente.objects.get(id=proceso['clienProv']),
                fecha=timezone.now(),
                total=total,
                emisor=request.user
            )
            crearReceta.save()
            print
            "Receta guardado"
            print
            crearReceta.id
            for k in proceso['medicamento']:
                medicamento = Medicamentos.objects.get(id=k['serial'])
                crearDetalle = DetalleReceta(
                    medicamento=medicamento,
                    descripcion=medicamento.nombre,
                    precio=medicamento.precio_venta,
                    cantidad=int(k['cantidad']),
                    impuesto=medicamento.igv * int(k['cantidad']),
                    subtotal=medicamento.precio_venta * int(k['cantidad']),
                    receta=crearReceta,
                )
                crearDetalle.save()

            messages.success(
                request, 'La venta se ha realizado satisfactoriamente')
        except Exception as e:
            try:
                transaction.savepoint_rollback(sid)
            except:
                pass
            messages.error(request, e)

    return render(request, 'receta/crear_receta.html', {'form': form})


# Busqueda de clientes para receta


def buscarCliente(request):
    idCliente = request.GET['id']
    cliente = Cliente.objects.filter(identificacion__contains=idCliente)
    data = serializers.serialize(
        'json', cliente, fields=('identificacion', 'nombres', 'apellidos', 'direccion', 'telefono'))
    return HttpResponse(data, content_type='application/json')


# Busqueda de medicamento para receta
def buscarMedicamento(request):
    idMedicamento = request.GET['id']
    medicamento = Medicamentos.objects.filter(nombre__contains=idMedicamento)
    data = serializers.serialize(
        'json', medicamento, fields=('code', 'stock', 'nombre', 'precio_venta', 'categoria', 'igv'))
    return HttpResponse(data, content_type='application/json')


def consultarReceta(request):
    receta = None
    detalles = None
    sum_subtotal = 0
    sum_tax = 0
    if request.method == 'POST':
        serie = request.POST.get('serie')
        numero = request.POST.get('num')

        receta = Receta.objects.get(serie=serie, numero=numero)
        detalles = DetalleReceta.objects.filter(receta=receta)

        for d in detalles:
            sum_tax = sum_tax + d.impuesto
        sum_subtotal = receta.total - sum_tax

    return render('receta/imprimir_receta.html',
                              {'receta': receta, 'detalles': detalles,
                               'sum_subtotal': sum_subtotal, 'sum_tax': sum_tax},
                              context_instance=RequestContext(request))


class ListaRecetas(ListView):
    template_name = 'receta/lista_venta.html'
    model = Receta

    def get_context_data(self, **kwargs):
        context = super(ListaRecetas, self).get_context_data(**kwargs)
        context['events'] = Receta.objects.filter(emisor=self.request.user)
        context['compras'] = context['events']
        context['paginate_by'] = context['events']
        return context


def write_pdf(template_src, context_dict):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return http.HttpResponse('Ocurrio un error al genera el reporte %s' % cgi.escape(html))


@login_required(login_url='/login')
def generar_pdf(request):
    receta = Receta.objects.all()

    if request.method == "POST":
        formbusqueda = RangoForm(request.POST)
        emisor = request.POST.get('emisor')

        if formbusqueda.is_valid():
            fecha_in = formbusqueda.cleaned_data['fecha_i']
            fecha_fi = formbusqueda.cleaned_data['fecha_f']
            rango = Receta.objects.filter(fecha__range=(fecha_in, fecha_fi)).filter(emisor__pk=request.user.id)

            total = 0
            for expe in rango:
                total = ((expe.total) + (total))

            return write_pdf('receta/reporte_receta.html', {'pagesize': 'legal', 'rango': rango, 'total': total})
            # return render_to_response ('empleados/test.html',{'rango':rango},context_instance=RequestContext(request))
        else:
            error = "Hay un error en las fechas proporcionadas"
            return render('receta/rango_reporte.html', {'error': error},
                                      context_instance=RequestContext(request))

    return render('receta/rango_reporte.html', {'rangoform': RangoForm()},
                              context_instance=RequestContext(request))


def reporteventas(request, pk):
    compra = Receta.objects.get(pk=pk)
    medicamentos = compra.receta.all()
    hora = datetime.today()

    return render('receta/reporte_venta.html', locals(), context_instance=ctx(request))
