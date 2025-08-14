import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()


class Settings:
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL", "postgresql://auth_user:auth_password@db:5432/auth_db")
        self.secret_key = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
        self.algorithm = os.getenv("ALGORITHM", "HS256")
        self.access_token_expire_minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


settings = Settings()
