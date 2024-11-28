from src.contrib.models import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey
from datetime import datetime


class AccountModel(BaseModel):
    __tablename__ = 'accounts'

    pk_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    balance: Mapped[str] = mapped_column(String, nullable=False)
    client: Mapped['ClientModel'] = relationship(back_populates='account')
    client_id: Mapped[int] = mapped_column(ForeignKey('clients.pk_id'))
