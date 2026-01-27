from django.urls import path
from . import views

urlpatterns = [
    path('', views.vista_mapa2, name='vistamapa2'),
    path('api/datos', views.api_estado_actual, name='estadoactual'),
    path('prueba/', views.vista_mapa2, name='vistamapa2' )
]