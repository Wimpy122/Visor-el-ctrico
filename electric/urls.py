from django.urls import path
from . import views

urlpatterns = [
    path('', views.vista_mapa, name='vistamapa'),
    path('api/datos', views.api_estado_actual, name='estadoactual')
]