# Auth Service

Сервис авторизации, построенный с использованием FastAPI, PostgreSQL и Docker.

## Быстрый старт

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
