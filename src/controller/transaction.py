from uuid import uuid4
from fastapi import APIRouter, Body, HTTPException, status, Depends
from datetime import datetime
from sqlalchemy import select, update, and_


from src.model.transactions import TransactionsModel
from src.model.account import AccountModel
from src.config.dependencies import DatabaseDependency
from src.schemas.transactions import TransactionSchemaIn, TransactionSchemaOut, TransactionTransaferSchemaIn, TransactionHistoricSchemaIn
from src.services.dbservices import add_transaction_history, get_account_by_secondary_id, get_accounts_by_secondary_id
from src.services.security import login_required

router = APIRouter(prefix="/transaction", tags=["transaction"])


@router.patch("/deposit")
async def account_deposit(
    db_session: DatabaseDependency,
    transaction_in: TransactionSchemaIn = Body(...),
    info=Depends(login_required)
) -> TransactionSchemaOut:
    transaction_out = TransactionSchemaOut(
        id=uuid4(),
        created_at=datetime.now(),
        type="deposit",
        to_account_id=transaction_in.from_account_id,
        **transaction_in.model_dump()
        )
    client_data = await get_account_by_secondary_id(db_session, AccountModel, transaction_out.from_account_id)

    if client_data.client_id == info["user_id"]:

        client_data.balance += transaction_out.balance

        await add_transaction_history(transaction_out, db_session, TransactionsModel, client_data.pk_id, client_data.pk_id)

        await db_session.commit()
        raise HTTPException(status_code=status.HTTP_200_OK)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.patch("/withdraw")
async def account_withdraw(
    db_session: DatabaseDependency,
    transaction_in: TransactionSchemaIn = Body(...),
    info=Depends(login_required)
) -> TransactionSchemaOut:
    transaction_out = TransactionSchemaOut(
        id=uuid4(),
        created_at=datetime.now(),
        type="withdraw",
        to_account_id=transaction_in.from_account_id,
        **transaction_in.model_dump()
        )
    client_data = await get_account_by_secondary_id(db_session, AccountModel, transaction_out.from_account_id)

    if client_data.client_id == info["user_id"]:
        client_data.balance -= transaction_out.balance

        await add_transaction_history(transaction_out, db_session, TransactionsModel, client_data.pk_id, client_data.pk_id)

        await db_session.commit()
        raise HTTPException(status_code=status.HTTP_200_OK)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.patch("/transfer")
async def account_transfer(
    db_session: DatabaseDependency,
    transfer_in: TransactionTransaferSchemaIn,
    info=Depends(login_required)
):
    transaction_out = TransactionSchemaOut(
            id=uuid4(),
            created_at=datetime.now(),
            type="transfer",
            **transfer_in.model_dump()
            )
    clients_data = await get_accounts_by_secondary_id(db_session, AccountModel, transaction_out.from_account_id, transaction_out.to_account_id)

    if clients_data[0][0].client_id == info["user_id"]:

        await add_transaction_history(transaction_out, db_session, TransactionsModel, clients_data[0][0].pk_id, clients_data[1].pk_id)

        clients_data[1].balance += transaction_out.balance
        clients_data[0][0].balance -= transaction_out.balance

        await db_session.commit()
        raise HTTPException(status_code=status.HTTP_200_OK)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


@router.get("/history", response_model=list[TransactionSchemaOut])
async def get_account_transaction(
        db_session: DatabaseDependency,
        info=Depends(login_required)
        ) -> list[TransactionSchemaOut]:
    historic: list[TransactionSchemaOut] = (await db_session.execute(select(TransactionsModel).join(AccountModel, AccountModel.pk_id == TransactionsModel.from_account_id).filter(AccountModel.client_id == info["user_id"]))).scalars().all()
    return historic
