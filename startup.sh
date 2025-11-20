#!/bin/bash
apt-get update
apt-get install -y unixodbc unixodbc-dev msodbcsql17
gunicorn app:app --bind=0.0.0.0 --timeout 600
