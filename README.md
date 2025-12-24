# 🌍 Travelia Backend

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Django](https://img.shields.io/badge/Django-REST_Framework-red)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon-336791)
![Gemini IA](https://img.shields.io/badge/AI-Gemini-orange)

Backend del proyecto **Travelia**, una aplicación inteligente para planificar viajes. Desarrollado con **Django REST Framework (DRF)**.

Este sistema utiliza **Inteligencia Artificial (Google Gemini)** para generar itinerarios personalizados, permite autenticación híbrida (Nativa + Google), gestiona preferencias de usuario (moneda/unidades) y almacena imágenes en la nube de forma optimizada.

Deploy oficial en **Render**.

---

## 📂 Estructura del proyecto

```bash
TRAVELIA-BACKEND/
├── ia/              # Servicio de comunicación con Gemini (Prompt engineering & Parsing)
├── media/           # Archivos temporales (Prod: Cloudinary)
├── medio/           # API para Medios de transporte
├── ruta/            # API para Rutas y tramos
├── travelia/        # Configuración core (Settings, URLs principales)
├── user/            # Autenticación (JWT), Perfil de usuario y Preferencias
├── viaje/           # Lógica de negocio: Planificación (IA) y Guardado de viajes
├── venv/            # Entorno virtual
├── .env             # Variables de entorno (no subir al repo)
├── manage.py
├── Procfile         # Configuración para Render
└── requirements.txt # Lista de dependencias
```

## ⚙️ Instalación y configuración
1. Clonar el repositorio
```bash
 git clone https://github.com/LautaRB/TravelIA-backend.git
 cd travelia-backend
```

2. Crear y activar entorno virtual
```bash
python -m venv venv

# En Windows:
venv\Scripts\activate

# En Mac/Linux:
source venv/bin/activate
```

3. Instalar dependencias
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno
Crea un archivo .env en la raíz del proyecto y copia el siguiente contenido, completando con tus credenciales:
```bash
# --- Django Core ---
SECRET_KEY=tu_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,.onrender.com

# --- Database (Neon/Postgres) ---
DATABASE_URL=postgresql://usuario:password@host:puerto/dbname

# --- Gemini AI ---
GEMINI_API_KEY=tu_api_key_de_google_ai

# --- Google OAuth (Login Social) ---
GOOGLE_CLIENT_ID=tu_google_client_id
GOOGLE_CLIENT_SECRET=tu_google_client_secret

# --- Cloudinary (Imágenes) ---
CLOUDINARY_CLOUD_NAME=tu_cloud_name
CLOUDINARY_API_KEY=tu_api_key
CLOUDINARY_API_SECRET=tu_api_secret
CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name
```

5. Migrar la base de datos
```bash
python manage.py migrate
```

6. Crear superusuario (Admin)
```bash
python manage.py createsuperuser
```

7. Ejecutar servidor
```bash
python manage.py runserver
```
El servidor correrá en: ```bash http://127.0.0.1:8000/ ```

## 🔑 Funcionalidades Principales
* **Planificación con IA:** Endpoint dedicado que consulta a Gemini para armar rutas, calcular distancias y estimar precios basándose en el origen/destino.
* **Gestión de Usuarios:** Registro y Login (JWT).
* **Login Social:** Integración con Google OAuth.
* **Perfil Completo:** Avatar personalizable (subida de imágenes con recorte), manejo de preferencias de moneda (USD/ARS/EUR) y unidad de distancia (KM/Millas).
* **Gestión de Imágenes:** Almacenamiento optimizado en Cloudinary.
* **Base de Datos:** Estructura relacional sólida en PostgreSQL (alojada en Neon).

## 📡 Endpoints
**Proximamente junto a la documentación**

## 🚀 Deploy
El proyecto cuenta con un archivo Procfile configurado para Render. La URL de producción es:
```bash
https://travelia-backend.onrender.com
```

## 📜 Licencia
Este proyecto está bajo la licencia MIT.

