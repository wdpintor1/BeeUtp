from django.contrib import admin
from django.urls import include, path
from . import views
from chart import views as chartViews

urlpatterns = [
    path('',views.chart),
    path("ws/chart/", views.chart, name="chart"),
    path('graficas_canal/<int:id_canal>/', chartViews.obtener_datos, name='graficas_canal'),    
    path('crear_grafica/<int:id_canal>/', chartViews.crear_grafica, name='crear_grafica'),  
    path("editar_visualizacion/<int:id_chart>/<int:id_canal>", views.editar_visualizacion, name="editar_visualizacion"),  
]