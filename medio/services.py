from .models import Medio

def crear_medio(medio_data):
    
    medio_obj, creado = Medio.objects.get_or_create(
        nombre_Medio=medio_data['nombre_Medio'],
        defaults={
            "tipo": medio_data.get('tipo', 'SIN DEFINIR'),
            "plataforma_recomendada": medio_data.get('plataforma_recomendada', '')
        }
    )
    
    return medio_obj, creado