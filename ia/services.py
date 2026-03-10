import google.generativeai as genai
import re
import json
from datetime import datetime
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-2.5-pro')
                            # gemini-2.5-pro version más potente
                            # gemini-2.5-flash version más rápida
def generar_plan_viaje(datos, user):
    # 1. Calculamos la cantidad de días
    dias_viaje = 1
    patron_fechas = re.findall(r'\d{4}-\d{2}-\d{2}', datos['rango_fechas'])
    if len(patron_fechas) == 2:
        try:
            inicio = datetime.strptime(patron_fechas[0], '%Y-%m-%d')
            fin = datetime.strptime(patron_fechas[1], '%Y-%m-%d')
            dias_viaje = (fin - inicio).days + 1
        except ValueError:
            pass

    # 2. El Prompt Definitivo actualizado
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

    TAREAS:
    1. Genera EXACTAMENTE 3 opciones de viaje utilizando ÚNICAMENTE la categoría de transporte elegida, diferenciadas por presupuesto (Alto, Medio, Bajo).
    2. Genera un itinerario sugerido enfocado 100% en el motivo '{datos['motivo_viaje']}'. 
       REGLA VITAL PARA EL ITINERARIO: Si el viaje dura más de 7 días, AGRUPA los días en el itinerario (Ej: "Días 1-3", "Días 4-6") para mantener la respuesta concisa. Si dura 7 días o menos, hazlo día por día.

    Reglas de Coherencia:
    - Sugerir alojamiento acorde al presupuesto.
    - Incluir plataformas web reales de compra.
    - Precios totales estimados.

    Estructura JSON estricta requerida:
    {{
        "opciones": [
            {{
                "categoria_presupuesto": "Alto",
                "titulo": "Título vendedor premium",
                "descripcion": "Justificación de por qué es la opción premium",
                "ruta": {{
                    "nombre": "Ruta específica",
                    "distancia": 1200,
                    "duracion_horas": 2
                }},
                "medio": {{
                    "nombre": "Vehículo exacto (ej: Vuelo Primera Clase / SUV Alta Gama)",
                    "tipo": "{datos['medio_transporte']}",
                    "precio_total": 15000,
                    "plataforma_recomendada": "Página web recomendada para comprar (ej: Despegar / Web oficial)"
                }},
                "alojamiento": {{
                    "tipo_sugerido": "Ej: Hotel 5 estrellas con pensión completa / Resort",
                    "plataforma_recomendada": "Página web recomendada (ej: Booking.com Premium / Hoteles.com)"
                }}
            }},
            {{
                "categoria_presupuesto": "Medio",
                "titulo": "Título vendedor estándar",
                "descripcion": "Justificación de la opción estándar",
                "ruta": {{
                    "nombre": "Ruta específica",
                    "distancia": 1200,
                    "duracion_horas": 2.5
                }},
                "medio": {{
                    "nombre": "Vehículo estándar",
                    "tipo": "{datos['medio_transporte']}",
                    "precio_total": 8000,
                    "plataforma_recomendada": "Página web recomendada para comprar"
                }},
                "alojamiento": {{
                    "tipo_sugerido": "Ej: Hotel 3 estrellas / Departamento entero",
                    "plataforma_recomendada": "Página web recomendada (ej: Airbnb / Booking.com)"
                }}
            }},
            {{
                "categoria_presupuesto": "Bajo",
                "titulo": "Título vendedor económico",
                "descripcion": "Justificación de la opción económica",
                "ruta": {{
                    "nombre": "Ruta específica",
                    "distancia": 1200,
                    "duracion_horas": 3.5
                }},
                "medio": {{
                    "nombre": "Vehículo económico",
                    "tipo": "{datos['medio_transporte']}",
                    "precio_total": 3000,
                    "plataforma_recomendada": "Página web recomendada para comprar"
                }},
                "alojamiento": {{
                    "tipo_sugerido": "Ej: Hostel compartido / Habitación privada económica",
                    "plataforma_recomendada": "Página web recomendada (ej: Hostelworld / Airbnb)"
                }}
            }}
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
    