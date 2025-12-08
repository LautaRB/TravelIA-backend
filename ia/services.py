import google.generativeai as genai
from django.conf import settings
import json
from ruta.services import crear_ruta
from medio.services import crear_medio

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-2.5-flash')
                            # gemini-2.5-pro version más potente
                            # gemini-2.5-flash version más rápida
def generar_plan_viaje(datos, user):
    moneda_pref = getattr(user, 'currency', 'ARS')
    unidad_pref = getattr(user, 'distance_unit', 'KM')
    
    nombre_moneda = "Dólares (USD)" if moneda_pref == 'USD' else "Pesos Argentinos (ARS)" if moneda_pref == 'ARS' else "Euros (EUR)"
    nombre_unidad = "Kilómetros" if unidad_pref == 'KM' else "Millas"
    
    prompt = f"""Hola! Quiero organizar un viaje del {datos['fecha_inicio']} al {datos['fecha_fin']}, partiendo desde {datos['origen']} hasta {datos['destino']}.
    Necesito que me recomiendes 3 rutas y 3 medios de transporte ideales para este recorrido.
    
    IMPORTANTE - PREFERENCIAS DEL USUARIO:
    - Precios: Expresar todos los costos en {nombre_moneda}.
    - Distancias: Expresar todas las distancias en {nombre_unidad}.
    
    Para cada ruta, incluí:
    1) Un nombre descriptivo,
    2) La distancia aproximada (solo el número),
    3) Y la duración estimada en horas.
    
    Para cada medio de transporte, indicá:
    1) El tipo de transporte (ej: TERRESTRE, AEREO, MARITIMO)
    2) Su nombre (ej: Auto, Avión, Buquebus)
    3) Y su precio aproximado.
    
    El JSON debe tener la siguiente estructura estricta:
    {{
        "rutas": [
            {{ "nombre": "Ruta 1", "distancia": 100, "duracion_horas": 5 }},
        ],
        "medios": [
            {{ "tipo": "TERRESTRE", "nombre": "Auto", "precio": 1000 }},
            ...
        ]
    }}
    
    Devolveme la respuesta exclusivamente en formato JSON válido, sin explicaciones ni texto adicional.
    """

    response = model.generate_content(prompt)
    
    texto = response.candidates[0].content.parts[0].text

    if texto.startswith("```json"):
        texto = texto.replace("```json", "").strip()
    if texto.endswith("```"):
        texto = texto[:-3].strip()

    try:
        contenido = json.loads(texto)
    except json.JSONDecodeError:
        return {"contenido": {"rutas": [], "medios": []}}
    
    return {
        "contenido": contenido,
    }
    