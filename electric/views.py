from django.shortcuts import render
from django.http import JsonResponse
from .models import RegistroGeneracion, Region 

def api_estado_actual(request):
    data = {}
    regiones = Region.objects.all()
    
    for reg in regiones:
        # CAMBIO AQUÍ: Usa el nuevo nombre también en la consulta
        ultimo_dato = RegistroGeneracion.objects.filter(region=reg).last()
        
        if ultimo_dato:
            data[reg.codigo_iso] = {
                "intensidad": ultimo_dato.intensidad_co2,
                "mix": {
                    "solar": ultimo_dato.solar,
                    "eolica": ultimo_dato.eolica,
                    "hidro": ultimo_dato.hidro,
                    "termo": ultimo_dato.termo
                }
            }
        else:
            data[reg.codigo_iso] = {"intensidad": 0, "mix": {}}
            
    return JsonResponse(data)

def vista_mapa(request):
    from django.shortcuts import render
    return render(request, 'index.html')

def vista_mapa2(request):
    from django.shortcuts import render
    return render(request, 'index_echarts.html')