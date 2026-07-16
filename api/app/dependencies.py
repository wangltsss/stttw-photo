from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import jwt
import uuid

from app.database import get_db
from app.models.user import User
from app.auth_utils import decode_access_token

http_bearer = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    db: AsyncSession = Depends(get_db)
) -> User:
    token = credentials.credentials
    try:
        user_id = decode_access_token(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = (await db.execute(select(User).where(uuid.UUID(user_id) == User.id))).scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user
