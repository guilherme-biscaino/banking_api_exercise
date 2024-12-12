from sqlalchemy import select


async def add_transaction_history(transaction_out, db, model, from_account_id, to_account_id=None):
    transaction_out.from_account_id, transaction_out.to_account_id = from_account_id, to_account_id

    db.add(model(**transaction_out.model_dump()))

    await db.commit()


async def get_account_by_secondary_id(db_session, model, from_account_id):

    return (await db_session.execute(select(model).filter_by(id=from_account_id))).scalars().first()


async def get_accounts_by_secondary_id(db_session, model, from_account_id, to_account_id):

    from_account = (await db_session.execute(select(model).filter_by(id=from_account_id))).scalars().all()

    to_account = (await db_session.execute(select(model).filter_by(id=to_account_id))).scalars().first()

    return [from_account, to_account]
