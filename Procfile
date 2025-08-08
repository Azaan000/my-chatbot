release: cd frontend && npm install && npm run build && cp -r build ../backend/static
web: gunicorn backend.app:app --bind 0.0.0.0:$PORT
