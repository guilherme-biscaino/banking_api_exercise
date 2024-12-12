from fastapi import APIRouter, HTTPException, status

from src.schemas.auth import LoginIn, LoginOut
from src.services.security import sign_jwt
from src.config.dependencies import DatabaseDependency
from src.services.dbservices import get_account_by_secondary_id
from src.model.client import ClientModel

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post('/login', response_model=LoginOut)
async def login(data: LoginIn, db_session: DatabaseDependency):

    client_data = await get_account_by_secondary_id(db_session, ClientModel, data.Account_id)

    if client_data.password == data.password:
        return sign_jwt(user_id=client_data.pk_id)

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account or password wrong.")