from .models import Medio
from travelia.utils.messeges import MessagesES

def crear_medio(medio):
    medio, creado = Medio.objects.get_or_create(
        nombre_Medio=medio['nombre_Medio'],
        tipo=medio['tipo'],
    )
    #Si creado es true, entonces se creo un nuevo medio
    #Si creado es false, entonces el medio ya existe
    if creado:
        print(MessagesES.SUCCESS_CREATE_MEDIA)
        return medio, creado
    else:
        print(MessagesES.ERROR_MEDIA_EXISTS)
        return medio, creado
        
    