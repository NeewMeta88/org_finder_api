
# 🏢 Organizations Directory API

RESTful API для поиска и получения структурированной информации об организациях, их зданиях и видах деятельности. Проект подходит для интеграции в корпоративные информационные системы, электронные справочники и веб‑порталы.

## ⚙️ Стек технологий

- Python 3.13
- FastAPI 0.116 (ASGI)
- SQLAlchemy 2 (async)
- PostgreSQL 15
- Alembic — миграции БД
- Docker + docker‑compose
- API‑ключи (заголовок `X‑API‑KEY`)

---

## 🚀 Быстрый старт

### 1. Клонировать репозиторий

```bash
git clone https://github.com/NeewMeta88/org_finder_api.git
cd org_finder_api
```

### 2. Создать виртуальное окружение (опционально)

```bash
python -m venv .venv
source .venv/bin/activate      # Windows → .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Подготовить файл `.env`
Пример содержимого (см. `.env.example`):

```
API_KEY=super‑secret‑key
DATABASE_URL=postgresql+asyncpg://user:pass@db:5432/db
POSTGRES_USER=user
POSTGRES_PASSWORD=pass
POSTGRES_DB=db
```

### 4. Запустить сервис

```bash
docker-compose up --build
```

Приложение будет доступно по адресу **http://localhost:8000**.  

### Документация
Swagger доступна по адресу **/docs**,  
альтернативная — **/redoc**.

---

### 5. Выполнить миграции
Выполните миграцию:
```bash
docker-compose run --rm web alembic upgrade head
```
Затем накатите (данные) для теста
```bash
docker-compose run --rm web python app/initial_data.py
```

---

## 🔑 Аутентификация

Для всех эндпоинтов требуется заголовок с API‑ключом:

```
X-API-KEY: super‑secret‑key
```

При отсутствии или неверном ключе сервер вернёт **401 Unauthorized**.

---

## 📚 API‑эндпоинты

| Метод   | URL                                       | Описание                                                               | Аутентификация |
| ------- | ----------------------------------------- | ---------------------------------------------------------------------- | -------------- |
| **GET** | `/organizations/`                         | Поиск организаций по фильтрам (`name`, `activity_id`)                  | ✅ Да           |
| **GET** | `/organizations/search`                   | Поиск организаций по геолокации (координаты или радиус)                | ✅ Да           |
| **GET** | `/organizations/{organization_id}`        | Детальная информация об организации                                    | ✅ Да           |
| **GET** | `/activities/{activity_id}/organizations` | Организации указанного вида деятельности (включая вложенные категории) | ✅ Да           |
| **GET** | `/buildings/{building_id}/organizations`  | Организации, расположенные в здании                                    | ✅ Да           |

### Параметры поиска организаций

| Параметр | Тип | Описание |
|----------|-----|----------|
| `name` | `str` | Подстрока для поиска по названию |
| `activity_id` | `int` | Фильтр по ID вида деятельности |
| `building_id` | `int` | Фильтр по ID здания |

---

## 💡 Бизнес‑правила

- Поиск чувствителен к регистру и выполняет LIKE‑сопоставление.
- При запросе организаций по виду деятельности учитываются вложенные категории до 3‑го уровня.
- Для лучшей производительности используется асинхронный доступ к БД и индексы по полям `name`, `activity_id`, `building_id`.

---

## 📎 Примеры cURL

**🔍 Поиск организаций по фильтрам (название и/или ID вида деятельности)**

```bash
curl -X GET "http://localhost:8000/organizations/?name=БетаКонсалт&activity_id=2" \
  -H "X-API-KEY: super-secret-key"
```

**📍 Поиск организаций по геолокации (радиус)**

```bash
curl -X GET "http://localhost:8000/organizations/search?lat=55.7605&lon=37.6402&radius=1" \
  -H "X-API-KEY: super-secret-key"
```

**🗺️ Поиск организаций по прямоугольной области**

```bash
curl -X GET "http://localhost:8000/organizations/search?lat_min=55.5&lat_max=56.6&lon_min=37.3&lon_max=38.4" \
  -H "X-API-KEY: super-secret-key"
```

**🏢 Организации в здании**

```bash
curl -X GET "http://localhost:8000/buildings/2/organizations" \
  -H "X-API-KEY: super-secret-key"
```

**⚙️ Организации по виду деятельности (включая вложенные)**

```bash
curl -X GET "http://localhost:8000/activities/3/organizations" \
  -H "X-API-KEY: super-secret-key"
```

**📝 Детали организации по ID**

```bash
curl -X GET "http://localhost:8000/organizations/1" \
  -H "X-API-KEY: super-secret-key"
```

---

## 🧪 Тестирование

```bash
docker-compose exec web pytest
```

Покрываются:
- сервисные слои (business‑logic)
- маршруты API

---

## 🗄 Миграции БД

```bash
# создание новой миграции
alembic revision -m "add new table"
# применение
alembic upgrade head
```

---

## 🧑‍💻 Автор

*Егор Родионов*