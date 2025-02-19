cd ..
source .venv/bin/activate
gunicorn --log-file gunicorn.log --bind 0.0.0.0:3300 --workers 3 app:app &
