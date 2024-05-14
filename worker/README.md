# Aplicação Worker
Aplicação para processamento de mensagens da fila SQS e envio de respostas para o Redis.

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

>Importante: O arquivo .env deve ser criado com as credenciais da OpenAI, na pasta raiz do dessa aplicação, conforme documentação da própria OpenAI disponível em https://beta.openai.com/docs/developer-quickstart/overview 

#### Exemplo de arquivo .env
```bash
OPENAI_API_KEY=sk-1234567890
```