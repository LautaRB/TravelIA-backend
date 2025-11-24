import google.generativeai as genai
from django.conf import settings
import json
from ruta.services import crear_ruta
from medio.services import crear_medio

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-2.5-flash')
                            # gemini-2.5-pro version más potente
                            # gemini-2.5-flash version más rápida
def generar_plan_viaje(datos):
    prompt = f"""Hola! Quiero organizar un viaje del {datos['fecha_inicio']} al {datos['fecha_fin']}, partiendo desde {datos['origen']} hasta {datos['destino']}.
    Necesito que me recomiendes 3 rutas y 3 medios de transporte ideales para este recorrido.
    Para cada ruta, incluí:
    1) Un nombre descriptivo,
    2) Los kilómetros aproximados del recorrido,
    3) Y la duración estimada en horas.
    
    Para cada medio de transporte, indicá:
    1) El tipo de transporte (ej: TERRESTRE, AEREO MARITIMO, etc.)
    2) Su nombre (ej: Auto, Avión, Buquebus, etc.)
    3) Y su precio en pesos argentinos.
    
    El JSON debe tener la siguiente estructura para las rutas y los medios, por ejemplo:
    
    rutas:
                nombre: Ruta 1,
                km: 100,
                duracion_horas: 5,
    "medios": [
                "tipo": "TERRESTRE",
                "nombre": "Auto",
                "precio": 1000,
    
    Devolveme la respuesta exclusivamente en formato JSON válido, sin explicaciones ni texto adicional.
    ¡Gracias!"""

    response = model.generate_content(prompt)
    
    texto = response.candidates[0].content.parts[0].text

    if texto.startswith("```json"):
        texto = texto.replace("```json", "").strip()
    if texto.endswith("```"):
        texto = texto[:-3].strip()

    contenido = json.loads(texto)
    
    print(contenido)
    
    rutas = [None] * len(contenido['rutas'])
    for i in range(len(contenido['rutas'])):
        rutas[i] = {
            "nombre_Ruta": contenido['rutas'][i]['nombre'],
            "origen": datos['origen'],
            "destino": datos['destino'],
            "km": contenido['rutas'][i]['km'],
            "tiempo": contenido['rutas'][i]['duracion_horas']
        }
    
    for ruta in rutas:
        crear_ruta(ruta)
    
    medios = [None] * len(contenido['medios'])
    for i in range(len(contenido['medios'])):
        medios[i] = {
            "tipo": contenido['medios'][i]['tipo'],
            "nombre_Medio": contenido['medios'][i]['nombre'],
            "precio": contenido['medios'][i]['precio']
        }
    
    for medio in medios:
        crear_medio(medio)
    
    return {
        "contenido": contenido,
    }
    