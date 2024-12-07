from fastapi import APIRouter

from servise.executor import create_user, create_operation, create_wallet

router = APIRouter()


@router.get('/user')
async def create_card():
    """Запрос добавление пользователя в базу"""
    result = await create_user()
    return result


@router.get('/wallet')
async def create_card():
    """Запрос добавления кошельков в базу"""
    result = await create_wallet()
    return result


@router.get('/operations')
async def create_card():
    """Запрос добавления операции в базу"""
    result = await create_operation()
    return result
