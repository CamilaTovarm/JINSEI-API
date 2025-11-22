#!/bin/bash

# Instalar dependencias del sistema
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
apt-get update
ACCEPT_EULA=Y apt-get install -y msodbcsql18

# Iniciar Gunicorn
gunicorn --bind=0.0.0.0 --timeout 600 app:app