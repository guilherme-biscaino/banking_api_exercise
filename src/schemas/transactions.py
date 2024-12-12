from typing import Annotated
from pydantic import Field, UUID4
from src.contrib.schemas import BaseSchema, BaseSchemaOut
from decimal import Decimal


class TransactionSchema(BaseSchema):
    balance: Annotated[Decimal, Field(description="Cliente que fará a transação")]

class TransactionSchemaIn(TransactionSchema):
    from_account_id: Annotated[UUID4, Field(description="id da conta")]

class TransactionHistoricSchemaIn(BaseSchema):
    from_account_id: Annotated[UUID4, Field(description="id da conta")]


class TransactionTransaferSchemaIn(TransactionSchemaIn):
    to_account_id: Annotated[UUID4, Field(description="id da conta")]

class TransactionSchemaOut(TransactionSchema, BaseSchemaOut):
    type: Annotated[str, Field(description="Cliente que fará a transação")]
    from_account_id: Annotated[int, Field(description="id da conta")]
    to_account_id: Annotated[int, Field(description="id da conta")]

