FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN opentelemetry-bootstrap --action=install

CMD opentelemetry-instrument --logs_exporter console,otlp \
    uvicorn src.main:app --port 8001 --host 0.0.0.0 