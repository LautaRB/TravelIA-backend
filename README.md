# 🌍 Travelia — Backend API

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Django REST Framework](https://img.shields.io/badge/Django-REST_Framework-092E20?logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon-336791?logo=postgresql&logoColor=white)
![Gemini AI](https://img.shields.io/badge/AI-Google_Gemini-FF6F00?logo=googlegemini&logoColor=white)

API RESTful para **Travelia**, una plataforma inteligente de planificación de viajes desarrollada como proyecto de tesis. Construida con **Django REST Framework (DRF)** y **PostgreSQL**.

El sistema integra **Google Gemini AI** para la generación automatizada de itinerarios a medida, implementa autenticación híbrida (JWT nativo + Google OAuth 2.0), gestiona preferencias regionales del usuario y optimiza el almacenamiento multimedia en la nube mediante **Cloudinary**.

> 🔗 **Repositorio Frontend:** [[TravelIA-Frontend]](https://github.com/LautaRB/TravelIA-frontend)

---

## 🔑 Funcionalidades Principales

- **Planificación Inteligente con IA:** Integración con la API de Google Gemini mediante *prompt engineering* y parseo estructurado para armar rutas, calcular distancias y estimar costos según origen y destino.
- **Autenticación Híbrida y Seguridad:** Flujo completo de registro y login mediante JSON Web Tokens (JWT) e integración con **Google OAuth 2.0**.
- **Gestión de Perfil y Preferencias:** Personalización de avatar (carga y recorte de imágenes en Cloudinary) y configuración de divisas (`ARS`, `USD`, `EUR`) y unidades de medida (`KM`, `Millas`).
- **Arquitectura Modular de Viajes:** Gestión relacional de itinerarios, tramos, rutas y medios de transporte persistidos en **PostgreSQL (Neon)**.

---

## 📂 Arquitectura del Proyecto

```text
TravelIA-backend/
├── ia/              # Servicio de integración con Gemini (Prompts y parseo de respuestas)
├── medio/           # Endpoints y modelos para medios de transporte
├── ruta/            # Gestión de rutas y tramos del itinerario
├── travelia/        # Configuración global del proyecto (Settings, URLs, WSGI)
├── user/            # Autenticación (JWT/OAuth), perfiles y preferencias de usuario
├── viaje/           # Lógica de negocio principal: planificación y persistencia de viajes
├── manage.py
├── Procfile         # Configuración de ejecución para producción (Gunicorn / Render)
└── requirements.txt # Dependencias del proyecto
```

---

## 📡 Endpoints Principales

| Módulo | Método | Endpoint (Ejemplo) | Descripción |
| :--- | :--- | :--- | :--- |
| **Auth / User** | `POST` | `/api/user/login/` | Autenticación JWT y login social con Google |
| **User** | `GET / PUT` | `/api/user/profile/` | Obtención y actualización de perfil, moneda y avatar |
| **IA** | `POST` | `/api/ia/planificar/` | Generación de itinerario sugerido vía Google Gemini |
| **Viajes** | `GET / POST` | `/api/viaje/` | Listado de viajes guardados y creación de nuevos itinerarios |
| **Rutas / Medios** | `GET` | `/api/ruta/` · `/api/medio/` | Consulta de tramos y medios de transporte disponibles |

---

## ⚙️ Instalación y Ejecución Local

### 1. Clonar el repositorio
```bash
git clone [https://github.com/LautaRB/TravelIA-backend.git](https://github.com/LautaRB/TravelIA-backend.git)
cd TravelIA-backend
```

### 2. Crear y activar el entorno virtual
```bash
python -m venv venv

# En Windows:
venv\Scripts\activate

# En Linux/macOS:
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Creá un archivo `.env` en la raíz del proyecto con la siguiente estructura:

```env
# --- Django Core ---
SECRET_KEY=tu_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# --- Database (PostgreSQL / Neon) ---
DATABASE_URL=postgresql://usuario:password@host:puerto/dbname

# --- Google Gemini AI ---
GEMINI_API_KEY=tu_api_key_de_google_ai

# --- Google OAuth 2.0 ---
GOOGLE_CLIENT_ID=tu_google_client_id
GOOGLE_CLIENT_SECRET=tu_google_client_secret

# --- Cloudinary ---
CLOUDINARY_CLOUD_NAME=tu_cloud_name
CLOUDINARY_API_KEY=tu_api_key
CLOUDINARY_API_SECRET=tu_api_secret
CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name
```

### 5. Ejecutar migraciones y levantar el servidor
```bash
python manage.py migrate
python manage.py createsuperuser # Opcional: para acceder al panel /admin
python manage.py runserver
```

El servidor estará disponible en `http://127.0.0.1:8000/`.

---

## 📜 Licencia
Distribuido bajo la licencia MIT.
