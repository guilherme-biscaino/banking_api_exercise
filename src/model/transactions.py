from src.contrib.models import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey
from datetime import datetime

from src.model.account import AccountModel


class TransactionsModel(BaseModel):
    __tablename__ = "transactions"

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(String, nullable=False)
    balance: Mapped[str] = mapped_column(String, nullable=False)

    from_account_id: Mapped['AccountModel'] = mapped_column(
        Integer, ForeignKey("accounts.pk_id")
    )
    to_account_id: Mapped['AccountModel'] = mapped_column(
        Integer, ForeignKey("accounts.pk_id"), unique=False
    )

    from_account = relationship(
        'AccountModel', foreign_keys='TransactionModel.from_account_id'
    )
    to_account = relationship(
        'AccountModel', foreign_keys='TransactionModel.to_account_id'
    )
