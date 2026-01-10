from django.db import models

# Create your models here.

class Region(models.Model):
    # Usaremos códigos ISO estandar (ej: CL-RM, CL-AN) para conectar facil con el GeoJSON
    codigo_iso = models.CharField(max_length=10, unique=True) 
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class RegistroGeneracion(models.Model):
    region = models.ForeignKey(Region, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    # Generación en MW (Simulados)
    solar = models.FloatField(default=0)
    eolica = models.FloatField(default=0)
    hidro = models.FloatField(default=0)
    termo = models.FloatField(default=0) # Carbón/Gas (Sucio)

    @property
    def total_mw(self):
        return self.solar + self.eolica + self.hidro + self.termo

    @property
    def intensidad_co2(self):
        # Fórmula simplificada: (Termo / Total) * Factor de emisión
        if self.total_mw == 0: return 0
        porcentaje_sucio = self.termo / self.total_mw
        # Digamos que la térmica emite 800g/kWh (promedio carbón/gas)
        return int(porcentaje_sucio * 800)