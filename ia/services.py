from openai import OpenAI
from django.conf import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def generar_plan_viaje(datos, user):
    prompt = f"""Hola! Quiero organizar un viaje del {datos['fecha_inicio']} al {datos['fecha_fin']}
    partiendo desde {datos['origen']} hasta {datos['destino']}.
    Por favor recomendame las 3 mejores rutas y los 3 mejores medios de transporte, además
    del tiempo que tomará cada ruta y los km del recorrido. Muchas gracias!"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Sos un asistente de viajes que da respuestas claras y útiles."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=600,
        temperature=0.7
    )

    contenido = response.choices[0].message.content

    tokens_usados = response.usage.total_tokens
    tokens_prompt = response.usage.prompt_tokens
    tokens_respuesta = response.usage.completion_tokens

    return {
        "plan": contenido,
        "tokens_usados": tokens_usados,
        "tokens_prompt": tokens_prompt,
        "tokens_respuesta": tokens_respuesta
    }
