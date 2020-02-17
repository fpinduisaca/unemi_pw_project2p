"""virtualpos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path

urlpatterns = [
    #path('clientes/', ClientesListView.as_view(), name='clientes-list'),
    path('clientes/', include('clientes.urls', namespace='clientes_app')),
    path('medicamentos/', include('medicamentos.urls', namespace='medicamentos_app')),
    path('recetas/', include('recetas.urls', namespace='receta_app')),
    # login-users
    path('', include('users.urls',  namespace='users_app')),
    path('admin/', admin.site.urls),
]
