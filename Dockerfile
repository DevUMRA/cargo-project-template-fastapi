# syntax=docker/dockerfile:1
# Qoldanba шаблонының Docker бейнесі. Талаптар: TEMPLATE.md («Docker бейнесі»).

FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PORT=8000

# curl — healthcheck үшін міндетті: Coolify және docker compose оны контейнер ішінде іске қосады
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Тәуелділіктер бөлек қабатта: код өзгергенде қайта орнатылмайды
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN chmod +x docker-entrypoint.sh

# root емес пайдаланушы
RUN useradd --system --uid 10001 --no-create-home app
USER 10001

EXPOSE 8000

HEALTHCHECK --interval=10s --timeout=3s --start-period=30s --retries=3 \
    CMD curl -fsS "http://127.0.0.1:${PORT}/health" || exit 1

ENTRYPOINT ["./docker-entrypoint.sh"]
# --proxy-headers: HTTPS-ті reverse proxy (Traefik / Cloudflare) береді, X-Forwarded-Proto сақталады
CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT} --proxy-headers --forwarded-allow-ips='*'"]
