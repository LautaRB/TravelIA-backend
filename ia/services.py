import google.generativeai as genai
from django.conf import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')
                            # gemini-1.5-pro version más potente

def generar_plan_viaje(datos, user):
    prompt = f"""Hola! Quiero organizar un viaje del {datos['fecha_inicio']} al {datos['fecha_fin']}
    partiendo desde {datos['origen']} hasta {datos['destino']}.
    Por favor recomendame las 3 mejores rutas y los 3 mejores medios de transporte, además
    del tiempo que tomará cada ruta y los km del recorrido. Muchas gracias!"""

    response = model.generate_content(prompt)

    contenido = response.text

    return {
        "plan": contenido,
        "tokens_usados": None,
        "tokens_prompt": None,
        "tokens_respuesta": None
    }
