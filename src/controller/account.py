from fastapi import APIRouter, Depends
from datetime import datetime
from uuid import uuid4

from sqlalchemy import select

from src.services.security import login_required
from src.config.dependencies import DatabaseDependency
from src.schemas.account import AccountSchemaOut, AccountSchemaIn, AccountSchemaOutPublic
from src.model.account import AccountModel


router = APIRouter(prefix="/account", tags=["account"])


@router.post('/create',
             response_model=AccountSchemaOut)
async def create_account(
    db_session: DatabaseDependency,
    info=Depends(login_required)
) -> AccountSchemaOut:
    account_out = AccountSchemaOut(id=uuid4(), client_id=info["user_id"], created_at=datetime.now(), balance=0)
    account_model = AccountModel(**account_out.model_dump())

    db_session.add(account_model)

    await db_session.commit()
    del account_out.client_id
    return account_out


@router.get("/list", response_model=list[AccountSchemaOutPublic])
async def get_all_accounts(
    db_session: DatabaseDependency,
    info=Depends(login_required)
) -> list[AccountSchemaOutPublic]:
    contas: list[AccountSchemaOutPublic] = (await db_session.execute(select(AccountModel).filter_by(client_id=info["user_id"]))).scalars().all()
    return contas


@router.delete("/delete")
async def delete_account(
    client_id: AccountSchemaIn,
    info=Depends(login_required)
):
    pass
