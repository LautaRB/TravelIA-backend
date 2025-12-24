from .models import Medio

def crear_medio(medio_data):
    
    medio_obj, creado = Medio.objects.get_or_create(
        nombre_Medio=medio_data['nombre_Medio'],
        defaults={
            "tipo": medio_data['tipo']
        }
    )
    
    return medio_obj, creado