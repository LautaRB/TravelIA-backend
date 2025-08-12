from .models import Ruta
from travelia.utils.messeges import MessagesES

def crear_ruta(ruta):
    ruta, creada = Ruta.objects.get_or_create(
        origen=ruta['origen'],
        destino=ruta['destino'],
        defaults={
            "nombre_Ruta": ruta['nombre_Ruta'],
            "km": ruta['km'],
            "tiempo": ruta['tiempo']
        }
    )
    
    #Si creada es true, entonces se creo una nueva ruta
    #Si creada es false, entonces la ruta ya existe
    if creada:
        print(MessagesES.SUCCESS_CREATE_ROUTE)
        return ruta, creada
    else:
        print(MessagesES.ERROR_ROUTE_EXISTS)
        return ruta, creada