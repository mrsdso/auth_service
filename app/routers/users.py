from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from ..database import get_db
from ..schemas import User, UserUpdate
from ..services.user_service import UserService
from .auth import get_current_active_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=User)
async def get_current_user_profile(
    current_user: User = Depends(get_current_active_user)
):
    """Получить профиль текущего пользователя"""
    return current_user


@router.put("/me", response_model=User)
async def update_current_user_profile(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Обновить профиль текущего пользователя"""
    user_service = UserService(db)
    
    try:
        updated_user = await user_service.update_user(current_user.id, user_data)
        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return updated_user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/me")
async def deactivate_current_user(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Деактивировать аккаунт текущего пользователя"""
    user_service = UserService(db)
    
    success = await user_service.deactivate_user(current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": "User account deactivated successfully"}
