from django.contrib import admin
from django.urls import path
from manage import views

urlpatterns = [
    path('',views.lista_canales),  
    path('lista_canales/', views.lista_canales, name='lista_canales'), 
    path('crear_canal/', views.crear_canal, name='crear_canal'),
    path('editar_canal/<int:id_canal>/', views.editar_canal, name='editar_canal'),
    path('eliminar_canal/<int:id_canal>/', views.eliminar_canal, name='eliminar_canal'),    
]