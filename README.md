# 🌍 Travelia Backend

Backend del proyecto **Travelia**, desarrollado con **Django REST Framework (DRF)**.  
Incluye autenticación con **JWT**, login/registro con **Google**, integración con **Gemini IA**, almacenamiento de imágenes en **Cloudinary** y base de datos en **PostgreSQL (Neon)**.  

Deploy oficial en **Render**.

---

## 📂 Estructura del proyecto

```bash
TRAVELIA-BACKEND/
├── ia/              # Lógica de integración con Gemini IA
├── media/           # Archivos subidos por usuarios (manejado por Cloudinary en producción)
├── medio/           # Módulo relacionado a medios de transporte
├── ruta/            # Gestión de rutas de viaje
├── static/          # Archivos estáticos
├── staticfiles/     # Archivos estáticos recolectados
├── travelia/        # Configuración principal del proyecto Django
├── user/            # Gestión de usuarios y autenticación (JWT + Google OAuth)
├── viaje/           # Módulo de planificación de viajes
├── venv/            # Entorno virtual local
├── .env             # Variables de entorno
├── .gitignore
├── manage.py
├── Procfile         # Configuración de despliegue en Render
├── README.md
└── requirements.txt # Dependencias del proyecto
```
## ⚙️ Instalación y configuración
### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/travelia-backend.git
cd travelia-backend
```
### 2. Crear y activar entorno virtual
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```
### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```
### 4. Configurar variables de entorno

 --- Gemini API ---
 - GEMINI_API_KEY=tu_api_key

 --- Google OAuth ---
- GOOGLE_CLIENT_ID=tu_google_client_id
- GOOGLE_CLIENT_SECRET=tu_google_client_secret

 --- Django ---
- SECRET_KEY=tu_secret_key
- DEBUG=True
- DEFAULT_PROFILE_PICTURE=tu_url_default_profile_picture

 --- PostgreSQL (Neon) ---
- DATABASE_URL=postgresql://usuario:password@host:puerto/dbname

 --- Render ---
- ALLOWED_HOSTS=localhost,127.0.0.1,.onrender.com

 --- Cloudinary ---
- CLOUDINARY_CLOUD_NAME=tu_cloud_name
- CLOUDINARY_API_KEY=tu_api_key
- CLOUDINARY_API_SECRET=tu_api_secret
- CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name

### 5. Migrar la base de datos
```bash
python manage.py migrate
```
### 6. Crear superusuario
```bash
python manage.py createsuperuser
```
### 7. Ejecutar servidor
```bash
python manage.py runserver
```
Servidor local: 👉 http://127.0.0.1:8000/

## 🔑 Funcionalidades principales
- Autenticación JWT para usuarios.
- Inicio de sesión con Google (Gmail) vía OAuth.
- Gemini IA integrada para procesamiento de datos inteligentes.
- Cloudinary para almacenamiento y gestión de imágenes.
- PostgreSQL (Neon) como base de datos principal.
- Deploy en Render con configuración lista (Procfile).

## 📖 Documentación de la API
Próximamente se agregará una colección de Postman para probar los endpoints.

## 🚀 Deploy en Render
Este proyecto está desplegado automáticamente en Render.
Cada push a la rama principal actualiza el backend en producción.
```bash
https://travelia-backend.onrender.com
```

## 📜 Licencia
Este proyecto está bajo la licencia MIT.
