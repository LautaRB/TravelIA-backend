from .models import Ruta

def crear_ruta(ruta_data):
    ruta, creada = Ruta.objects.get_or_create(
        nombre_Ruta=ruta_data['nombre_Ruta'],
        defaults={
            "origen": ruta_data['origen'],
            "destino": ruta_data['destino'],
            "distancia": ruta_data['distancia'],
            "tiempo": ruta_data['tiempo']
        }
    )
    
    return ruta, creada