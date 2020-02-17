from django.urls import path
from . import views

app_name = 'recetas'
urlpatterns = [
    path('', views.ListaRecetas.as_view(), name='lista_ventas'),
    path('create/', views.recetaCrear, name="emitir_receta"),
    path('buscar_cliente/', views.buscarCliente),
    path('buscar_medicamento/', views.buscarMedicamento),
    path('consultar/', views.consultarReceta, name="consultar_receta"),
    path('generar_reporte_receta/', views.generar_pdf, name='generar_reporte_recetas'),
    path('reporte_recetas/<int:pk>/', views.reporteventas, name='reporte_ventas'),
]
