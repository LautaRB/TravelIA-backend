import google.generativeai as genai
from django.conf import settings
import json

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-2.5-pro')
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
            
            Planifica un viaje desde '{datos['origen']}' hasta '{datos['destino']}'.
            - Periodo de viaje deseado: {datos['rango_fechas']}.
            - Cantidad de pasajeros: {datos['cantidad_personas']}.
            - Medio de transporte elegido: {datos['medio_transporte']} (Opciones válidas: TERRESTRE, MARITIMO, AEREA).

            Genera EXACTAMENTE 3 opciones de viaje utilizando ÚNICAMENTE la categoría de transporte elegida.
            Las 3 opciones deben diferenciarse estrictamente por su presupuesto: Alto, Medio y Bajo.
            
            Reglas de Coherencia y Recomendaciones:
            - El vehículo sugerido debe corresponder a la categoría '{datos['medio_transporte']}' y tener capacidad para {datos['cantidad_personas']} personas.
            - DEBES sugerir un tipo de alojamiento acorde al nivel de presupuesto de la opción.
            - DEBES incluir recomendaciones reales de las mejores páginas web o plataformas donde el usuario puede ir a comprar/reservar tanto el transporte como el alojamiento (Ej: Booking, Airbnb, Despegar, Skyscanner, Central de Pasajes, etc.).
            - El precio debe ser el costo TOTAL estimado para todas las personas (Transporte + Alojamiento).
            
            IMPORTANTE - PREFERENCIAS DEL USUARIO:
            - Precios estimados TOTALES: {nombre_moneda} (Solo el número).
            - Distancias: {nombre_unidad} (Solo el número).

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
    