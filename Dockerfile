FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends gcc python3-dev libssl-dev curl && \
    rm -rf /var/lib/apt/lists/* && \
    python -m pip install --upgrade pip setuptools wheel && \
    groupadd -r appgroup && \
    useradd -r -g appgroup appuser

COPY requirements.txt .

RUN python -m pip install --no-cache-dir --upgrade -r requirements.txt && \
    python -m pip check && \
    python -m pip show cryptography && \
    rm -f /usr/local/lib/python3.12/site-packages/pip/_vendor/bom.cdx.json

COPY . .

RUN chown -R appuser:appgroup /app

USER appuser

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]