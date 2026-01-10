import google.generativeai as genai
from django.conf import settings
import json

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-2.5-flash')
                            # gemini-2.5-pro version más potente
                            # gemini-2.5-flash version más rápida
def generar_plan_viaje(datos, user):
    moneda_pref = getattr(user, 'currency', 'ARS')
    unidad_pref = getattr(user, 'distance_unit', 'KM')
    
    nombre_moneda = "Dólares (USD)" if moneda_pref == 'USD' else "Pesos Argentinos (ARS)" if moneda_pref == 'ARS' else "Euros (EUR)"
    nombre_unidad = "Kilómetros" if unidad_pref == 'KM' else "Millas"
    
    prompt = f"""
    Actúa como un agente de viajes experto. 
    
    VALIDACIÓN PREVIA:
    Si '{datos['origen']}' o '{datos['destino']}' NO son lugares geográficos reales o coherentes, 
    devuelve un JSON con una lista "opciones" vacía: {{ "opciones": [] }}.
    
    Planifica un viaje desde '{datos['origen']}' hasta '{datos['destino']}' 
    para las fechas: {datos['fecha_inicio']} a {datos['fecha_fin']}.

    Genera EXACTAMENTE 3 opciones de viaje distintas y lógicas.
    Cada opción debe ser un paquete cerrado que combine una RUTA específica con un MEDIO DE TRANSPORTE coherente para esa ruta.
    
    Reglas de Coherencia:
    - Si la ruta es aérea, el medio debe ser Avión.
    - Si la ruta es terrestre, el medio debe ser Auto, Bus o Tren.
    
    IMPORTANTE - PREFERENCIAS DEL USUARIO:
    - Precios estimados: {nombre_moneda} (Solo el número).
    - Distancias: {nombre_unidad} (Solo el número).

    Estructura JSON estricta requerida:
    {{
        "opciones": [
            {{
                "titulo": "Título vendedor (ej: La Opción Rápida)",
                "descripcion": "Breve explicación de por qué elegir esto",
                "ruta": {{
                    "nombre": "Nombre de la ruta (ej: Vía Aérea / Ruta Nac. 9)",
                    "distancia": 1200,
                    "duracion_horas": 2
                }},
                "medio": {{
                    "nombre": "Vehículo (ej: Boeing 737 / Bus Cama)",
                    "tipo": "AEREO" o "TERRESTRE",
                    "precio": 5000
                }}
            }}
        ]
    }}
    
    Devolveme la respuesta exclusivamente en formato JSON válido, sin explicaciones ni texto adicional ni bloques de código markdown.
    """

    try:
        response = model.generate_content(prompt)
        texto = response.text
        
        if "```json" in texto:
            texto = texto.replace("```json", "").replace("```", "").strip()
        elif "```" in texto:
            texto = texto.replace("```", "").strip()

        contenido = json.loads(texto)
        if "opciones" not in contenido:
            contenido = {"opciones": []}

        return {"contenido": contenido}

    except Exception as e:
        print(f"Error en servicio IA: {str(e)}")
        return {"contenido": {"opciones": []}}
    