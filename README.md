<div align="center">
https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi
https://img.shields.io/badge/FastStream-005571?style=for-the-badge&logo=fastapi
https://img.shields.io/badge/TaskIQ-FF6F00?style=for-the-badge&logo=task
https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white
https://img.shields.io/badge/redis-%2523DD0031.svg?style=for-the-badge&logo=redis&logoColor=white
https://img.shields.io/badge/RabbitMQ-FF6600?style=for-the-badge&logo=rabbitmq&logoColor=white

</div>

# Orders API

Базовый проект для развёртывания 2 сущностей: API + Event bus Consumer.\
В качестве базы данных используется Postgres.\
В качестве кэширование + прослеживание лимит запросов используется Redis.\
В качестве передатчика данных используется Rabbitmq.


## Поднятие проекта

### Переменные окружения

```shell
# Конфиги подключения к Postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5435
POSTGRES_DB=orders
POSTGRES_PASSWORD=LyhaEkM2D6TeH96W8jxG
POSTGRES_USER=orders_user
PGUSER=orders_user
POSTGRES_TRANSACTION_TIMEOUT=30 # Время ожиданий обработки в БД
POSTGRES_ECHO=true # Флаг показа логов SqlAlchemy

# Конфиги подключения к RabbitMQ
RMQ_USER=user
RMQ_PASSWORD=bitnami
RMQ_HOST=localhost
RMQ_PORT=5672
RMQ_VHOST=%2f
RMQ_PARAMS=connection_attempts=3&heartbeat=60
RMQ_EXCHANGE=test # Название обменника в RMQ
RMQ_QUEUE=test # Название очереди в RMQ

# Конфиги подключения к Redis
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=12345
REDIS_USER=user
REDIS_USER_PASSWORD=12345
REDIS_TTL_EXPIRE=30 # Время жизни кэша в секундах

# Настройки Токена
JWT_SECRET_KEY="Somesecretkey" # Секрета расшифровки токена
JWT_ALGORITHM="HS256" # Алгоритма кодировки токена
JWT_LIFETIME=10 # время жизни токена в минутах

# Настройки проекта
ENV_ALLOWED_ORIGINS="*" # Допустимые внешние домены для запросов
API_PORT=8000  # Внешний порт сервера

LOGLEVEL=INFO
```

### Команда разворота сервиса

```shell
docker compose up -d --build
```

На случае, если внешние порты нужно отрегулировать, это можно сделать через `*_PORT` для каждого сервиса.
*Рекомендации*: Данный сервис тестовый. В случае развёртывания на прод лучше закрыть все порты и использовать для API прокси через `NGINX`