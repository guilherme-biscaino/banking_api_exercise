from typing import Annotated
from pydantic import Field, UUID4
from decimal import Decimal
from datetime import datetime
from src.contrib.schemas import BaseSchema, BaseSchemaOut


class AccountSchema(BaseSchema):
    pass


class AccountSchemaIn(AccountSchema):
    id: Annotated[UUID4, Field(description="Identifier")]
    pass


class AccountSchemaOut(AccountSchema, BaseSchemaOut):
    balance: Annotated[Decimal, Field(description="Salda da conta")]
    client_id: Annotated[int, Field(description="id do client")]
    pass


class AccountSchemaOutPublic(AccountSchema, BaseSchema):
    id: Annotated[UUID4, Field(description="Identifier")]
    balance: Annotated[Decimal, Field(description="Salda da conta")]
    created_at: Annotated[datetime, Field(description="Data de criação")]
