FROM node:22-bookworm-slim AS ui
WORKDIR /ui
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

FROM python:3.13-slim-bookworm
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 STACK_FRONTEND_DIST=/app/frontend/dist
COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt
COPY backend/app /app/backend/app
COPY backend/data /app/backend/data
COPY backend/migrations /app/backend/migrations
COPY backend/setup_local.py backend/setup_server.py /app/backend/
COPY --from=ui /ui/dist /app/frontend/dist
RUN useradd --create-home stack
USER stack
CMD ["sh", "-c", "exec uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port ${PORT:-8000} --workers 1 --no-access-log"]
