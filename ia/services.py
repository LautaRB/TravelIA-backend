import google.generativeai as genai
import re
import json
from datetime import datetime
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-2.5-pro')

def generar_plan_viaje(datos, user):
    dias_viaje = 1
    patron_fechas = re.findall(r'\d{4}-\d{2}-\d{2}', datos['rango_fechas'])
    if len(patron_fechas) == 2:
        try:
            inicio = datetime.strptime(patron_fechas[0], '%Y-%m-%d')
            fin = datetime.strptime(patron_fechas[1], '%Y-%m-%d')
            dias_viaje = (fin - inicio).days + 1
        except ValueError:
            pass

    moneda_usuario = getattr(user, 'currency', None) or 'ARS'

    prompt = f"""
    Actúa como un agente de viajes experto. 
    
    VALIDACIÓN PREVIA:
    Si '{datos['origen']}' o '{datos['destino']}' NO son lugares geográficos reales o coherentes, 
    devuelve un JSON con una lista "opciones" vacía y un "itinerario" vacío.
    
    Planifica un viaje desde '{datos['origen']}' hasta '{datos['destino']}'.
    - Periodo de viaje: {datos['rango_fechas']} (Total: {dias_viaje} días).
    - Cantidad de pasajeros: {datos['cantidad_personas']}.
    - Medio de transporte: {datos['medio_transporte']} (Opciones: TERRESTRE, MARITIMO, AEREA).
    - Motivo del viaje: {datos['motivo_viaje']}.
    - Moneda obligatoria para todos los precios: {moneda_usuario}.

    TAREAS:
    1. Genera EXACTAMENTE 3 opciones de viaje utilizando ÚNICAMENTE la categoría de transporte elegida, diferenciadas por presupuesto (Alto, Medio, Bajo).
    2. Genera un itinerario sugerido enfocado 100% en el motivo '{datos['motivo_viaje']}'. 
       REGLA VITAL PARA EL ITINERARIO: Si el viaje dura más de 7 días, AGRUPA los días en el itinerario (Ej: "Días 1-3", "Días 4-6"). Si dura 7 días o menos, hazlo día por día.

    REGLAS ESTRICTAS DE PRECIOS Y COHERENCIA:
    - ABSOLUTAMENTE TODOS los valores numéricos de precio DEBEN estar en la moneda {moneda_usuario}, teniendo en cuenta la economía real y actual para esa moneda.
    - Coherencia de Alojamiento (Sugerencias tipo Booking.com): 
      * Opción "Alto": Hoteles 4/5 estrellas, resorts de lujo o alojamientos premium.
      * Opción "Medio": Hoteles 3 estrellas, departamentos enteros cómodos.
      * Opción "Bajo": Hostels compartidos, pensiones o habitaciones privadas económicas.
    - Fórmula de Precio Total: Debes desglosar mentalmente y sumar:
      (Precio Transporte total por 1 persona * {datos['cantidad_personas']}) + (Precio de 1 Noche de Hotel * {dias_viaje}). 
      Ese cálculo final debe ir en el campo "precio_total_opcion".

    Estructura JSON estricta requerida:
    {{
        "opciones": [
            {{
                "categoria_presupuesto": "Alto",
                "titulo": "Título vendedor premium",
                "descripcion": "Justificación de por qué es la opción premium",
                "precio_total_opcion": 1500000, 
                "ruta": {{
                    "nombre": "Ruta específica",
                    "distancia": 1200,
                    "duracion_horas": 2
                }},
                "medio": {{
                    "nombre": "Vuelo Primera Clase",
                    "tipo": "{datos['medio_transporte']}",
                    "precio_total_pasajeros": 500000,
                    "plataforma_recomendada": "Ej: Despegar / Web oficial"
                }},
                "alojamiento": {{
                    "tipo_sugerido": "Hotel 5 estrellas con pensión completa",
                    "precio_total_estadia": 1000000,
                    "plataforma_recomendada": "Booking.com Premium"
                }}
            }},
            // REPETIR LA MISMA ESTRUCTURA PARA LAS OPCIONES "Medio" y "Bajo", ajustando precios ({moneda_usuario}) y gama del hotel.
        ],
        "itinerario": [
            {{
                "dia": "Día 1 (o Días 1-3)",
                "titulo": "Título de la actividad principal",
                "actividades": "Descripción de lo que van a hacer enfocado en {datos['motivo_viaje']}",
                "tip_presupuesto": "Un consejo de ahorro o lujo para este día"
            }}
        ]
    }}
    
    Devuelve la respuesta exclusivamente en formato JSON válido, sin explicaciones ni texto adicional ni bloques de código markdown.
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