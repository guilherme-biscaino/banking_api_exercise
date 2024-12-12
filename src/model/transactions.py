from src.contrib.models import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey, DECIMAL
from datetime import datetime
from decimal import Decimal
from pydantic import UUID4

from src.model.account import AccountModel


class TransactionsModel(BaseModel):
    __tablename__ = "transactions"

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    type: Mapped[str] = mapped_column(String, nullable=False)
    balance: Mapped[Decimal] = mapped_column(DECIMAL, nullable=False)

    from_account_id: Mapped[int] = mapped_column(
         Integer, ForeignKey("accounts.pk_id")
     )
    to_account_id: Mapped[int] = mapped_column(
         Integer, ForeignKey("accounts.pk_id")
    )

    from_account = relationship("AccountModel", foreign_keys="[TransactionsModel.from_account_id]")
    to_account = relationship("AccountModel", foreign_keys="[TransactionsModel.to_account_id]")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # from_account_id: Mapped[UUID4] = mapped_column(
    #     Integer, nullable=False
    # )
    # to_account_id: Mapped[UUID4] = mapped_column(
    #     Integer, nullable=False
    # )
