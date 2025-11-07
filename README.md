# Documentación del Proyecto: Masvida Roadmap

## Descripción General
Este proyecto es una aplicación web para gestionar y visualizar un roadmap (hoja de ruta) utilizando Flask como backend y una interfaz web. La aplicación permite gestionar módulos, sprints y estados, con integración a Google Sheets para el almacenamiento de datos.

## Tecnologías Utilizadas
- **Backend**: Python con Flask
- **Almacenamiento**: 
  - JSON local (`roadmap_data.json`)
  - Google Sheets (integración)
- **Dependencias Principales**:
  - Flask 3.0.3
  - gspread 6.1.4
  - google-auth 2.35.0
  - gunicorn 21.2.0

## Estructura del Proyecto
```
├── app.py              # Archivo principal de la aplicación Flask
├── data.json           # Archivo de almacenamiento local JSON
├── requirements.txt    # Dependencias del proyecto
├── Procfile           # Configuración para despliegue
├── masvida_roadmap.html # Interfaz de usuario
└── roadmap_data.json   # Datos del roadmap
```

## Funcionalidades Principales

### 1. Gestión de Datos
- Carga y guardado de datos en formato JSON local
- Sincronización automática con Google Sheets
- Estructura de datos que incluye:
  - Módulos
  - Sprints
  - Estados
  - Duración
  - Vistas personalizadas

### 2. API Endpoints

#### GET Endpoints
- `/`: Sirve la página principal (masvida_roadmap.html)
- `/load`: Carga los datos del roadmap
- `/vistas`: Obtiene las vistas guardadas

#### POST Endpoints
- `/save`: Guarda los datos del roadmap
- `/vistas`: Guarda nuevas vistas
- `/save_states`: Guarda los estados del roadmap

### 3. Integración con Google Sheets
- Utiliza credenciales de servicio para autenticación
- Sincronización automática de datos
- Estructura de hoja: Módulo, Sprint, Duración

## Configuración

### Variables de Entorno Requeridas
- `GOOGLE_CREDENTIALS`: Credenciales de servicio de Google (JSON)

### Configuración de Google Sheets
- ID de la hoja: `1y2jRf9G6WzHWDCoER7gjrEKL4LoepRuHdk5fsctzgNo`
- Alcance de permisos: `https://www.googleapis.com/auth/spreadsheets`

## Estructura de Datos
```json
{
  "data": [],           // Datos principales del roadmap
  "estados": [],        // Estados disponibles
  "meses": [],         // Configuración de meses
  "cantidadSprints": 16, // Número total de sprints
  "vistas": []         // Vistas personalizadas guardadas
}
```

## Despliegue
El proyecto está configurado para ser desplegado en Render usando gunicorn como servidor WSGI.

## Características del Sistema
- Soporte para múltiples vistas del roadmap
- Gestión flexible de estados
- Sincronización en tiempo real con Google Sheets
- Capacidad para manejar hasta 16 sprints
- Almacenamiento local y en la nube

## Mantenimiento
- Los datos se guardan automáticamente en ambos sistemas (JSON local y Google Sheets)
- La sincronización es bidireccional para mantener la integridad de los datos
- El sistema mantiene un respaldo local en caso de problemas de conectividad

---
Para más detalles específicos sobre la implementación de la interfaz de usuario o configuraciones adicionales, se recomienda revisar el archivo `masvida_roadmap.html`.