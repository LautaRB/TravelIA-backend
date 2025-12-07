from .models import Ruta
from travelia.utils.messeges import MessagesES

def crear_ruta(ruta):
    ruta, creada = Ruta.objects.get_or_create(
        nombre_Ruta=ruta['nombre_Ruta'],
        defaults={
            "origen":ruta['origen'],
            "destino":ruta['destino'],
            "distancia": ruta['distancia'],
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