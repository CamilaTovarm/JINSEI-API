
apt-get update
gunicorn app:app --bind=0.0.0.0 --timeout 600
