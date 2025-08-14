# Auth Service

Сервис авторизации, построенный с использованием FastAPI, PostgreSQL и Docker.

## Особенности

- **FastAPI** для создания REST API
- **PostgreSQL** в качестве базы данных
- **JWT** токены для аутентификации
- **BCrypt** для хеширования паролей
- **Docker** для контейнеризации
- **Pydantic** для валидации данных
- **SQLAlchemy** для работы с базой данных

## Быстрый старт

### Использование Docker Compose (рекомендуется)

1. Клонируйте репозиторий и перейдите в директорию проекта:
```bash
cd auth_service
```

2. Скопируйте файл с переменными окружения:
```bash
copy .env.example .env
```

3. Запустите сервисы:
```bash
docker-compose up --build
```

Сервис будет доступен по адресу: http://localhost:8000

### Локальная разработка

1. Создайте виртуальное окружение:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Запустите PostgreSQL (через Docker):
```bash
docker run --name auth_db -e POSTGRES_DB=auth_db -e POSTGRES_USER=auth_user -e POSTGRES_PASSWORD=auth_password -p 5432:5432 -d postgres:15
```

4. Запустите приложение:
```bash
uvicorn app.main:app --reload
```

## API Endpoints

### Аутентификация

- `POST /auth/register` - Регистрация нового пользователя
- `POST /auth/token` - Получение JWT токена (логин)
- `GET /auth/me` - Получение информации о текущем пользователе
- `POST /auth/logout` - Выход из системы

### Пользователи

- `GET /users/me` - Получение профиля текущего пользователя
- `PUT /users/me` - Обновление профиля текущего пользователя
- `DELETE /users/me` - Деактивация аккаунта текущего пользователя

### Служебные

- `GET /` - Корневой endpoint
- `GET /health` - Проверка здоровья сервиса
- `GET /docs` - Swagger документация
- `GET /redoc` - ReDoc документация

## Примеры использования

### Регистрация пользователя

```bash
curl -X POST "http://localhost:8000/auth/register" \
     -H "Content-Type: application/json" \
     -d '{
       "username": "testuser",
       "email": "test@example.com",
       "password": "testpassword"
     }'
```

### Получение токена

```bash
curl -X POST "http://localhost:8000/auth/token" \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=testuser&password=testpassword"
```

### Использование токена

```bash
curl -X GET "http://localhost:8000/auth/me" \
     -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Безопасность

- Пароли хешируются с использованием BCrypt
- JWT токены подписываются секретным ключом
- Валидация данных на уровне Pydantic схем
- CORS 
