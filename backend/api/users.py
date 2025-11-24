import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import get_db
from backend.core.exceptions import ModelExistsError
from backend.models.user_model import UserModel
from backend.schemas.user_schema import UserCreateRequest, User

router = APIRouter()

logger = logging.getLogger(__name__)

@router.post(
    "/register",
    response_model=User,
    status_code=status.HTTP_201_CREATED
)
async def register_user(
        data: UserCreateRequest,
        session: AsyncSession = Depends(get_db),
) -> User:
    try:
        return await User.create(session, data)
    except ModelExistsError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="User already exists"
        )


# @router.get("/{telegram_id}", response_model=User)
# async def get_user(telegram_id: int, session: AsyncSession = Depends(get_db)):
#      obj = await User.get(session, telegram_id, field=telegram_id)
#      return
    # result = await db.scalars(select(UserModel).where(UserModel.telegram_id == telegram_id))
    # user = result.first()
    # return UserIdResponse.model_validate(user)
