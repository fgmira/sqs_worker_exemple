FROM python:3.11-slim

WORKDIR /worker

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN opentelemetry-bootstrap --action=install

CMD opentelemetry-instrument --logs_exporter console,otlp \
    python src/main.py