from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import auth_router, users_router
from .database import engine, Base

app = FastAPI(
    title="Auth Service",
    description="Сервис авторизации с использованием FastAPI и PostgreSQL",
    version="1.0.0"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене следует указать конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(auth_router)
app.include_router(users_router)


@app.on_event("startup")
async def startup_event():
    """Создание таблиц при запуске приложения"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    """Корневой endpoint"""
    return {"message": "Auth Service API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """Проверка здоровья сервиса"""
    return {"status": "healthy"}
