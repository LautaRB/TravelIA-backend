from .models import Ruta

def crear_ruta(ruta):
    ruta, creada = Ruta.objects.get_or_create(
        viaje_id=ruta['viaje_id'],
        origen=ruta['origen'],
        destino=ruta['destino'],
        defaults={
            "nombre_Ruta": ruta['nombre_Ruta'],
            "km": ruta['km'],
            "tiempo": ruta['tiempo']
        }
    )
    
    if creada:
        print("Ruta creada")
    else:
        print("Ya existe esta ruta")

    return ruta