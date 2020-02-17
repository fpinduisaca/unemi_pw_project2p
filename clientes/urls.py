from django.urls import path

from . import views

app_name = 'clientes'
urlpatterns = [
    path('', views.ClientesListView.as_view(), name='list_clientes'),
    # path('list/', views.ClientesListView.as_view(), name='list_clientes'),
    path('detail/<int:pk>/', views.ClientesDetailView.as_view(), name='detail_clientes'),
    path('create/', views.ClientesCreateView.as_view(), name='create_clientes'),
    path('update/<int:pk>/', views.ClientesUpdateView.as_view(), name='update_clientes'),
    path('delete/<int:pk>/', views.ClientesDeleteView.as_view(), name='delete_clientes'),
]
