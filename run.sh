source .venv/bin/activate
gunicorn --bind 0.0.0.0:3300 --workers 1 app:app &