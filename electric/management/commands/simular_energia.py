import random
from django.core.management.base import BaseCommand
from electric.models import Region, RegistroGeneracion

class Command(BaseCommand):
    help = 'Genera datos simulados realistas para el sistema eléctrico de Chile'

    def handle(self, *args, **options):
        # 1. Lista de regiones con su "perfil energético"
        # Perfiles: 'norte' (solar), 'centro' (mixto), 'sur' (hidro/viento)
        regiones_config = [
            {'iso': 'CL-AP', 'nombre': 'Arica y Parinacota', 'perfil': 'norte'},
            {'iso': 'CL-TA', 'nombre': 'Tarapacá', 'perfil': 'norte'},
            {'iso': 'CL-AN', 'nombre': 'Antofagasta', 'perfil': 'norte'},
            {'iso': 'CL-AT', 'nombre': 'Atacama', 'perfil': 'norte'},
            {'iso': 'CL-CO', 'nombre': 'Coquimbo', 'perfil': 'norte'},
            {'iso': 'CL-VS', 'nombre': 'Valparaíso', 'perfil': 'centro'},
            {'iso': 'CL-RM', 'nombre': 'Metropolitana', 'perfil': 'centro'},
            {'iso': 'CL-LI', 'nombre': 'O Higgins', 'perfil': 'centro'},
            {'iso': 'CL-ML', 'nombre': 'Maule', 'perfil': 'sur'},
            {'iso': 'CL-NB', 'nombre': 'Ñuble', 'perfil': 'sur'},
            {'iso': 'CL-BI', 'nombre': 'Biobío', 'perfil': 'sur'},
            {'iso': 'CL-AR', 'nombre': 'Araucanía', 'perfil': 'sur'},
            {'iso': 'CL-LR', 'nombre': 'Los Ríos', 'perfil': 'sur'},
            {'iso': 'CL-LL', 'nombre': 'Los Lagos', 'perfil': 'sur'},
            {'iso': 'CL-AI', 'nombre': 'Aysén', 'perfil': 'sur'},
            {'iso': 'CL-MA', 'nombre': 'Magallanes', 'perfil': 'sur'},
        ]

        self.stdout.write("Iniciando simulación de la red eléctrica...")

        for config in regiones_config:
            # Crear región si no existe
            region, _ = Region.objects.get_or_create(
                codigo_iso=config['iso'], 
                defaults={'nombre': config['nombre']}
            )

            # Generar valores según el perfil geográfico
            solar, eolica, hidro, termo = 0, 0, 0, 0

            if config['perfil'] == 'norte':
                solar = random.uniform(200, 800)  # Mucho sol
                eolica = random.uniform(50, 300)
                hidro = random.uniform(0, 50)     # Casi nada de agua
                termo = random.uniform(300, 900)  # Termoeléctricas mineras

            elif config['perfil'] == 'centro':
                solar = random.uniform(100, 400)
                eolica = random.uniform(50, 200)
                hidro = random.uniform(200, 600)  # Centrales de pasada
                termo = random.uniform(100, 500)

            elif config['perfil'] == 'sur':
                solar = random.uniform(0, 100)    # Poco sol
                eolica = random.uniform(200, 600) # Mucho viento
                hidro = random.uniform(500, 1000) # Grandes represas
                termo = random.uniform(50, 200)   # Poca termo (generalmente biomasa)

            # Guardar el registro simulado
            registro = RegistroGeneracion.objects.create(
                region=region,
                solar=round(solar, 1),
                eolica=round(eolica, 1),
                hidro=round(hidro, 1),
                termo=round(termo, 1)
            )

            # Imprimir feedback visual en la consola
            estado = "VERDE" if registro.intensidad_co2 < 200 else "SUCIO"
            self.stdout.write(f"-> {region.nombre}: {registro.intensidad_co2}g CO2/kWh ({estado})")

        self.stdout.write(self.style.SUCCESS("¡Simulación completada! Datos listos en DB."))