import openai
from django.conf import settings

openai.api_key = settings.OPENAI_API_KEY

def generar_plan_viaje(datos, user):
    prompt = f"""Hola! Quiero organizar un viaje del {datos['fecha_inicio']} al {datos['fecha_fin']}
    partiendo desde {datos['origen']} hasta {datos['destino']}.
    Por favor recomendame las 3 mejores rutas y los 3 mejores medios de transporte, además
    del tiempo que tomará cada ruta y los km del recorrido. Muchas gracias!"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"username": {user.username}, "role": "user", "content": prompt}]
    )

    contenido = response['choices'][0]['message']['content']
    return {"plan": contenido}
