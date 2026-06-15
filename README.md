# Global Delivery

Микросервис для Службы международной доставки. Принимает данные о посылках, рассчитывает стоимость доставки на основе веса, стоимости содержимого и текущего курса доллара ЦБ РФ.

## Стек технологий

- **FastAPI** — веб-фреймворк (async)
- **SQLAlchemy 2.0** (async) — ORM
- **PostgreSQL** — основная база данных
- **Alembic** — миграции
- **Redis** — брокер сообщений для Celery и кеш курса валют
- **Celery** + **Celery Beat** — периодические задачи
- **httpx** — асинхронные HTTP-запросы (получение курса ЦБ)
- **Pydantic v2** — валидация данных
- **pytest** — тестирование

## Структура проекта

```
app/
├── api/v1/routers/     # эндпоинты FastAPI
├── core/               # конфигурация, логирование, сессии
├── db/                 # подключение к БД и Redis
├── models/             # SQLAlchemy ORM модели
├── schemas/            # Pydantic схемы (request/response)
├── repositories/       # слой доступа к данным (DAL)
├── services/           # бизнес-логика
├── tasks/              # Celery задачи
├── integrations/       # внешние сервисы (ЦБ РФ)
└── main.py             # точка входа

alembic/                # миграции БД
tests/                  # тесты
docker-compose.yml
Dockerfile
.env.example
```

## Запуск проекта

### 1. Клонировать репозиторий

```bash
git clone <repo_url>
cd GlobalDeliveryPetProject
```

### 2. Создать `.env` файл

Скопируй `.env.example` в `.env` и заполни значения:

```bash
cp .env.example .env
```

### 3. Запустить через Docker Compose

```bash
docker-compose up --build
```

Сервис будет доступен по адресу: `http://localhost:8000`

Swagger-документация: `http://localhost:8000/docs`

## API эндпоинты

| Метод | Путь | Описание |
|-------|------|----------|
| `POST` | `/api/v1/parcels/` | Зарегистрировать посылку |
| `GET` | `/api/v1/parcels/` | Получить список своих посылок (с пагинацией и фильтрами) |
| `GET` | `/api/v1/parcels/{parcel_id}` | Получить посылку по id |
| `GET` | `/api/v1/parcel-types/` | Получить список типов посылок |

## Сессии

Авторизация в проекте не используется. Каждый пользователь идентифицируется по `session_id`, который автоматически устанавливается в cookie при первом запросе. Все посылки привязываются к этому `session_id`.

## Периодические задачи

Раз в 5 минут Celery Beat запускает задачу расчёта стоимости доставки для всех необработанных посылок:

```
Стоимость = (вес в кг * 0.5 + стоимость содержимого в долларах * 0.01) * курс USD/RUB
```

Курс доллара берётся с [cbr-xml-daily.ru](https://www.cbr-xml-daily.ru/daily_json.js) и кешируется в Redis на время, указанное в `USD_RATE_CACHE_TTL`.

### Запуск задачи вручную (для отладки)

```bash
docker-compose exec celery celery -A app.tasks.celery_app call app.tasks.calculate_costs.calculate_delivery_costs
```

## Миграции

Применить миграции:

```bash
docker-compose exec app alembic upgrade head
```

Создать новую миграцию:

```bash
docker-compose exec app alembic revision --autogenerate -m "description"
```

## Тесты

```bash
pytest -v
```

## Переменные окружения

См. `.env.example` для полного списка. Основные:

- `POSTGRES_*` — настройки подключения к PostgreSQL
- `REDIS_BROKER` — брокер Celery
- `REDIS_CACHE` — кеш курса валют
- `USD_RATE_CACHE_TTL` — время жизни кеша курса (сек)
- `API_PREFIX` — префикс API (по умолчанию `/api/v1`)
