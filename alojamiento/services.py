from .models import Alojamiento

def crear_alojamiento(alojamiento_data):
    alojamiento_obj, creado = Alojamiento.objects.get_or_create(
        tipo_sugerido=alojamiento_data.get('tipo_sugerido', 'No especificado'),
        defaults={
            "plataforma_recomendada": alojamiento_data.get('plataforma_recomendada', '')
        }
    )
    return alojamiento_obj, creado