from django.urls import path, re_path

from . import views

app_name = 'users'
urlpatterns = [
    path('', views.userlogin, name='login'),
    path('logout/', views.LogOut, name='logout'),
    path('home/', views.Home.as_view(), name='home'),
    # path('<int:pk>/', views.DetailView.as_view(), name='detail'),
]