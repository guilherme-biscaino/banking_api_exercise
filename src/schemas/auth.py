from typing import Annotated
from pydantic import UUID4, Field


from src.contrib.schemas import BaseSchema


class LoginIn(BaseSchema):
    Account_id: Annotated[UUID4, Field(description="id da conta")]
    password: Annotated[str, Field(description="senha da conta")]


class LoginOut(BaseSchema):
    access_token: str
