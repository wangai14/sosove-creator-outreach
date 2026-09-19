FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY . /app

EXPOSE 8796

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8796/api/health', timeout=3).read()"

CMD ["python", "-m", "instagram_creator_outreach.server", "--host", "0.0.0.0", "--port", "8796"]
