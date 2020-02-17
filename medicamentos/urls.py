from django.urls import path

from . import views

app_name = 'medicamentos'
urlpatterns = [
    path('', views.ListaMedicamentos.as_view(), name='list_medicamentos'),
    path('detail/<int:pk>/', views.DetalleView.as_view(), name='detail_medicamentos'),
    path('create/', views.CreateMedicamentos.as_view(), name='create_medicamentos'),
    path('update/<int:pk>/', views.ActualizarView.as_view(), name='update_medicamentos'),
    path('delete/<int:pk>/', views.EliminarView.as_view(), name='delete_medicamentos'),
    path('reporte/', views.generar_reporte_medicamentos, name='reporte'),
    path('presentacion', views.CreatePresentacion.as_view(), name='create_presentacion'),
]