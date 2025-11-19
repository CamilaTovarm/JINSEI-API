# JINSEI

JINSEI es una aplicación web desarrollada en Python utilizando Flask como framework principal. El proyecto implementa una arquitectura de microservicios para gestionar diferentes aspectos de la aplicación.

## 🚀 Características

- Gestión de usuarios y sesiones
- Sistema de contactos y tipos de contactos
- Manejo de documentos y tipos de documentos
- Sistema de consentimientos
- Evaluación de niveles de riesgo
- Mensajería integrada
- Soft delete implementado para todas las entidades

## 🛠️ Tecnologías

- Python
- Flask
- SQLAlchemy
- Alembic (para migraciones)
- SQL Server (Base de datos)
- Swagger (Documentación API)

## 📁 Estructura del Proyecto

```
├── Controllers/         # Controladores de la API
├── Models/             # Modelos de datos
├── Repositories/       # Capa de acceso a datos
├── Services/          # Lógica de negocio
├── migrations/        # Archivos de migración de base de datos
├── app.py            # Punto de entrada de la aplicación
├── ConfigDB.py       # Configuración de la base de datos
└── SwaggerConf.py    # Configuración de Swagger
```

## 🚦 Primeros Pasos

1. Clonar el repositorio:
```bash
git clone https://github.com/tuusuario/JINSEI.git
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Configurar la base de datos en `ConfigDB.py`

4. Ejecutar migraciones:
```bash
flask db upgrade
```

5. Iniciar la aplicación:
```bash
python app.py
```

## 📚 Documentación API

La documentación de la API está disponible a través de Swagger UI cuando la aplicación está en ejecución:
```
http://localhost:5000/swagger/
```