# App para exposição de API's
Aplicação basica em FastAPI para exposição de API's de postagem de perguntas e respostas.

## Endpoints
- [GET] /health -> Retorna um status 200
- [POST] /question -> Envia uma pergunta para a fila
- [POST] /answer -> Recebe uma resposta de uma pergunta

## Variáveis de Ambiente (Vide DockerCompose)
- Variaveis de ambiente para o OpenTelemetry
    - OTEL_EXPORTER_OTLP_INSECURE
    - OTEL_EXPORTER_OTLP_ENDPOINT
    - OTEL_METRICS_EXPORTER
    - OTEL_LOGS_EXPORTER
    - OTEL_PYTHON_LOGGING_AUTO_INSTRUMENTATION_ENABLED
    - OTEL_SERVICE_NAME
    - OTEL_METRIC_EXPORT_INTERVAL
    - COLLECTOR_OTLP_ENABLED
- Variaveis de ambiente para LocalStack
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
    - AWS_DEFAULT_REGION
    - ENDPOINT_URL
- Variaveis gerais da Aplicação
    - QUEUE_NAME: Nome da fila criada no sqs
    - LOG_LEVEL: Nivel de log
    - REDIS_HOST: Host do Redis
    - REDIS_PORT: Porta do Redis
    - REDIS_PASSWORD: Senha do Redis




