# FastAPI Demo Backend

## функционал

регистрация пользователей
авторизация через jwt токены
создание задач
просмотр списка задач
просмотр отдельной задачи
обновление задачи
удаление задачи

данные хранятся в памяти и будут потеряны при перезапуске сервера

## установка

```bash
pip install -r requirements.txt
```

## запуск

```bash
uvicorn app.main:app --reload
```

сервер запустится на http://localhost:8000

документация доступна на http://localhost:8000/docs

## запуск через docker

```bash
docker-compose up --build
```

## тесты

```bash
pytest tests/
```

## примеры использования

### регистрация

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

ответ содержит access_token который нужно использовать для авторизованных запросов

### авторизация

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

### создание задачи

```bash
curl -X POST "http://localhost:8000/tasks" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "title": "новая задача",
    "description": "описание задачи"
  }'
```

### получение списка задач

```bash
curl -X GET "http://localhost:8000/tasks" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### получение задачи по id

```bash
curl -X GET "http://localhost:8000/tasks/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### обновление задачи

```bash
curl -X PUT "http://localhost:8000/tasks/1" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{
    "title": "обновленный заголовок",
    "completed": true
  }'
```

### удаление задачи

```bash
curl -X DELETE "http://localhost:8000/tasks/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## структура проекта

```
app/
  main.py      основной файл приложения с эндпоинтами
  models.py    модели данных
  schemas.py   pydantic схемы для валидации
  crud.py      функции для работы с данными
  db.py        хранение данных в памяти

tests/
  test_basic.py  базовые тесты

requirements.txt  зависимости проекта
Dockerfile       образ для docker
docker-compose.yml  конфигурация docker compose
```
