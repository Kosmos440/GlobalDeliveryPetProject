# Global Delivery

Сервис для Службы международной доставки. Принимает данные о посылках, рассчитывает стоимость доставки на основе веса, стоимости содержимого и текущего курса доллара ЦБ РФ.

## Стек технологий

- **FastAPI** — веб-фреймворк (async)
- **SQLAlchemy 2.0** (async) — ORM
- **PostgreSQL** — основная база данных
- **Alembic** — миграции
- **Redis** — брокер сообщений для Celery и кеш курса валют
- **Celery** + **Celery Beat** — периодические задачи
- **httpx** — асинхронные HTTP-запросы (получение курса ЦБ)
- **Pydantic v2** — валидация данных
- **uv** — менеджер пакетов и виртуальных окружений
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
pyproject.toml          # зависимости и конфигурация инструментов
uv.lock                 # версии зависимостей
docker-compose-local.yaml
Dockerfile
.env.example
```

## Локальная разработка

### 1. Установить uv

Если uv ещё не установлен на машине:

```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Для Linux/macOS:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Клонировать репозиторий

```bash
git clone https://github.com/Kosmos440/GlobalDeliveryPetProject
cd GlobalDeliveryPetProject
```

### 3. Создать `.env` файл

Скопируй `.env.example` в `.env` и заполни значения:

```bash
cp .env.example .env
```

### 4. Установить зависимости

```bash
uv sync
```

Эта команда сама создаст виртуальное окружение `.venv` и установит все зависимости строго по `uv.lock`. Отдельно активировать окружение не обязательно — все команды ниже запускаются через `uv run`.

### 5. Запустить сервис локально

```bash
uv run uvicorn app.main:app --reload
```

Сервис будет доступен по адресу: `http://localhost:8000`

## Запуск через Docker Compose

```bash
docker compose -f docker-compose-local.yaml up --build
```

Swagger-документация: `http://localhost:8000/docs`

Фронтенд: `http://localhost:8000/ui`

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

В Docker:

```bash
docker compose -f docker-compose-local.yaml exec celery-worker celery -A app.tasks.celery_app call app.tasks.calculate_costs.calculate_delivery_costs
```

Локально:

```bash
uv run celery -A app.tasks.celery_app call app.tasks.calculate_costs.calculate_delivery_costs
```

## Миграции

Применить миграции:

```bash
# в Docker
docker compose -f docker-compose-local.yaml exec fastapi alembic upgrade head

# локально
uv run alembic upgrade head
```

Создать новую миграцию:

```bash
uv run alembic revision --autogenerate -m "description"
```

## Тесты

```bash
uv run pytest -v
```

## Линтинг и форматирование

```bash
uv run ruff check .
uv run ruff format .
uv run mypy
```

## Управление зависимостями

```bash
uv add <package>              # добавить зависимость
uv add --dev <package>        # добавить dev-зависимость
uv remove <package>           # удалить зависимость
uv lock --upgrade             # обновить все версии в uv.lock до последних совместимых
uv sync                       # переустановить окружение по uv.lock
```

`uv.lock` коммитится в git — он фиксирует точные версии зависимостей для воспроизводимых сборок у всех разработчиков и в CI/Docker. Файл `.venv/` в git не попадает, он указан в `.gitignore`.

## Переменные окружения

См. `.env.example` для полного списка. Основные:

- `POSTGRES_*` — настройки подключения к PostgreSQL
- `REDIS_BROKER` — брокер Celery
- `REDIS_CACHE` — кеш курса валют
- `USD_RATE_CACHE_TTL` — время жизни кеша курса (сек)
- `API_PREFIX` — префикс API (по умолчанию `/api/v1`)
