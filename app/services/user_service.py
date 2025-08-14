from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from typing import Optional

from ..models.user import User
from ..schemas import UserCreate, UserUpdate
from ..utils.security import get_password_hash, verify_password


class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Получить пользователя по ID"""
        result = await self.db.execute(select(User).filter(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> Optional[User]:
        """Получить пользователя по имени пользователя"""
        result = await self.db.execute(select(User).filter(User.username == username))
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Получить пользователя по email"""
        result = await self.db.execute(select(User).filter(User.email == email))
        return result.scalar_one_or_none()

    async def create_user(self, user_data: UserCreate) -> User:
        """Создать нового пользователя"""
        hashed_password = get_password_hash(user_data.password)
        
        db_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password
        )
        
        try:
            self.db.add(db_user)
            await self.db.commit()
            await self.db.refresh(db_user)
            return db_user
        except IntegrityError:
            await self.db.rollback()
            raise ValueError("Пользователь с таким именем или email уже существует")

    async def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Обновить данные пользователя"""
        db_user = await self.get_user_by_id(user_id)
        if not db_user:
            return None

        update_data = user_data.dict(exclude_unset=True)
        
        if "password" in update_data:
            update_data["hashed_password"] = get_password_hash(update_data.pop("password"))

        for field, value in update_data.items():
            setattr(db_user, field, value)

        try:
            await self.db.commit()
            await self.db.refresh(db_user)
            return db_user
        except IntegrityError:
            await self.db.rollback()
            raise ValueError("Пользователь с таким именем или email уже существует")

    async def authenticate_user(self, username: str, password: str) -> Optional[User]:
        """Аутентификация пользователя"""
        user = await self.get_user_by_username(username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    async def deactivate_user(self, user_id: int) -> bool:
        """Деактивировать пользователя"""
        db_user = await self.get_user_by_id(user_id)
        if not db_user:
            return False
        
        db_user.is_active = False
        await self.db.commit()
        return True
