# TasteAPI

**TasteAPI** — это REST API для управления заказами еды в ресторане, построенный на **FastAPI** с использованием **PostgreSQL**, **SQLAlchemy**, **Alembic** и **Docker**. Проект реализован по принципам **Onion Architecture**, что обеспечивает модульность, читаемость и расширяемость кода. API позволяет управлять блюдами и заказами, включая создание, просмотр, отмену заказов и изменение их статусов с соблюдением бизнес-логики.

## Основные возможности

- **Управление блюдами**:
  - Получение списка всех блюд (`GET /dishes/`).
  - Добавление нового блюда (`POST /dishes/`).
  - Удаление блюда (`DELETE /dishes/{id}`).
- **Управление заказами**:
  - Получение списка всех заказов (`GET /orders/`).
  - Создание заказа с проверкой существования блюд (`POST /orders/`).
  - Отмена заказа (только в статусе "в обработке") (`DELETE /orders/{id}`).
  - Изменение статуса заказа с последовательной валидацией (`PATCH /orders/{id}/status`).
- **Бизнес-логика**:
  - Проверка существования блюд при создании заказа.
  - Ограничение отмены заказов только для статуса "в обработке".
  - Последовательное изменение статусов: `в обработке` → `готовится` → `доставляется` → `завершен`.
- **Технические особенности**:
  - Использует **FastAPI** для высокопроизводительного API.
  - **PostgreSQL** и асинхронный **SQLAlchemy** для работы с базой данных.
  - **Alembic** для управления миграциями.
  - **Docker** и **docker-compose** для контейнеризации.
  - Логгирование операций с помощью модуля `logging`.
  - Тестирование с использованием **pytest** и **pytest-asyncio**.
  - Линтер **Ruff** для проверки качества кода.

## Требования

- **Python** 3.10+
- **Docker** и **docker-compose**
- **PostgreSQL** 13+
- **uv** (для управления зависимостями)

## Установка и запуск

### 1. Клонирование репозитория
```bash
git clone https://github.com/<your-username>/TasteAPI.git
cd TasteAPI
```

### 2. Настройка переменных окружения
Создайте файл `.env` на основе `.env.example`:
```
MODE=DEV
DB_USER=postgres
DB_PASS=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=dev_db
```

Для тестов создайте `.test.env`:
```
MODE=TEST
DB_USER=postgres
DB_PASS=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=test_db
```

### 3. Установка зависимостей
Установите **uv** и зависимости:
```bash
pip install uv
uv venv
source .venv/bin/activate  # Для Linux/Mac
.venv\Scripts\activate     # Для Windows
uv pip install -r pyproject.toml
```

### 4. Запуск приложения
Используйте **docker-compose** для запуска приложения и базы данных:
```bash
docker-compose up -d
```

### 5. Применение миграций
Создайте и примените миграции базы данных:
```bash
docker-compose exec app alembic upgrade head
```

### 6. Доступ к API
API доступно по адресу: `http://localhost:8000/docs` (Swagger UI).

## Примеры API-запросов

### 1. Получение списка блюд
```bash
curl -X GET "http://localhost:8000/dishes/"
```
**Ответ**:
```json
[
  {
    "id": 1,
    "name": "Пицца Маргарита",
    "description": "Классическая пицца с томатами и моцареллой",
    "price": 500.0,
    "category": "Основные блюда"
  }
]
```

### 2. Создание блюда
```bash
curl -X POST "http://localhost:8000/dishes/" \
-H "Content-Type: application/json" \
-d '{
  "name": "Пицца Маргарита",
  "description": "Классическая пицца с томатами и моцареллой",
  "price": 500.0,
  "category": "Основные блюда"
}'
```
**Ответ**:
```json
{
  "id": 1,
  "name": "Пицца Маргарита",
  "description": "Классическая пицца с томатами и моцареллой",
  "price": 500.0,
  "category": "Основные блюда"
}
```

### 3. Создание заказа
```bash
curl -X POST "http://localhost:8000/orders/" \
-H "Content-Type: application/json" \
-d '{
  "customer_name": "Иван",
  "dish_ids": [1]
}'
```
**Ответ**:
```json
{
  "id": 1,
  "customer_name": "Иван",
  "dish_ids": [1],
  "order_time": "2025-06-18T19:14:00",
  "status": "в обработке",
  "dishes": [
    {
      "id": 1,
      "name": "Пицца Маргарита",
      "description": "Классическая пицца с томатами и моцареллой",
      "price": 500.0,
      "category": "Основные блюда"
    }
  ]
}
```

### 4. Изменение статуса заказа
```bash
curl -X PATCH "http://localhost:8000/orders/1/status" \
-H "Content-Type: application/json" \
-d '{"status": "готовится"}'
```
**Ответ**:
```json
{
  "id": 1,
  "customer_name": "Иван",
  "dish_ids": [1],
  "order_time": "2025-06-18T19:14:00",
  "status": "готовится",
  "dishes": [
    {
      "id": 1,
      "name": "Пицца Маргарита",
      "description": "Классическая пицца с томатами и моцареллой",
      "price": 500.0,
      "category": "Основные блюда"
    }
  ]
}
```

### 5. Отмена заказа
```bash
curl -X DELETE "http://localhost:8000/orders/1"
```
**Ответ**:
```json
{
  "id": 1,
  "customer_name": "Сергей",
  "dish_ids": [1],
  "order_time": "2025-06-18T19:14:00",
  "status": "в обработке",
  "dishes": [
    {
      "id": 1,
      "name": "Пицца Маргарита",
      "description": "Классическая пицца с томатами и моцареллой",
      "price": 500.0,
      "category": "Основные блюда"
    }
  ]
}
```

## Тестирование

1. Настройте тестовую базу данных в `.test.env` (см. выше).
2. Установите зависимости для разработки:
   ```bash
   uv pip install --system ".[dev]"
   ```
3. Запустите тесты:
   ```bash
   pytest --maxfail=1 -vv
   ```

## Команды для разработчиков

- **Создание миграции**:
  ```bash
  alembic revision --autogenerate -m "Описание миграции"
  ```
- **Применение миграций**:
  ```bash
  alembic upgrade head
  ```
- **Откат миграций**:
  ```bash
  alembic downgrade -1
  ```
- **Проверка кода с линтером**:
  ```bash
  ruff check . --config=pyproject.toml
  ```

## Структура проекта

```
.
├── alembic/
│   ├── versions/
│   └── env.py
├── src/
│   ├── api/v1/
│   │   ├── routers/
│   │   │   ├── dishes.py
│   │   │   └── orders.py
│   │   └── services/
│   │       ├── dishes.py
│   │       └── orders.py
│   ├── database/
│   │   └── db.py
│   ├── models/
│   │   ├── dish.py
│   │   └── order.py
│   ├── repositories/
│   │   ├── dish.py
│   │   └── order.py
│   ├── schemas/
│   │   ├── dish.py
│   │   └── order.py
│   ├── utils/
│   │   └── logger.py
│   ├── config.py
│   ├── main.py
│   └── metadata.py
├── tests/
│   ├── fixtures/
│   │   ├── db_mocks/
│   │   └── testing_cases/
│   ├── unit/
│   │   ├── api/
│   │   └── repositories/
│   ├── integration/
│   ├── migration/
│   ├── conftest.py
│   ├── constants.py
│   └── utils.py
├── .env
├── .test.env
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── README.md
```

- **src/**: Основная директория приложения.
  - **api/v1/**: Маршруты и сервисы API.
  - **database/**: Настройка базы данных.
  - **models/**: ORM-модели SQLAlchemy.
  - **repositories/**: Логика работы с базой данных.
  - **schemas/**: Pydantic-схемы для валидации.
  - **utils/**: Вспомогательные функции (логгирование).
  - **config.py**: Настройки приложения.
  - **main.py**: Точка входа FastAPI.
- **alembic/**: Миграции базы данных.
- **tests/**: Юнит- и интеграционные тесты.

## Зависимости

Зависимости указаны в `pyproject.toml`. Установите их с помощью **uv**:
```bash
uv pip install -r pyproject.toml
```

## Возможные улучшения

- **Аутентификация**: Добавить JWT для защиты API.
- **Пагинация**: Реализовать пагинацию для списков блюд и заказов.
- **Кэширование**: Использовать Redis для кэширования частых запросов.
- **CI/CD**: Настроить GitHub Actions для автоматического тестирования и деплоя.

## Контакты

Для вопросов и предложений: [your-email@example.com]