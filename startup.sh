#!/bin/bash
# Instala dependencias del sistema
apt-get update
apt-get install -y unixodbc unixodbc-dev msodbcsql17

# Instala las dependencias de Python
pip install -r requirements.txt

# Levanta la app con gunicorn
gunicorn --bind 0.0.0.0:8000 app:app
