from typing import Annotated
from pydantic import Field
from src.contrib.schemas import BaseSchema, BaseSchemaOut
from datetime import datetime


class ClientSchema(BaseSchema):
    cpf: Annotated[str, Field(description="Cpf do cliente", examples=["23158946746"], max_length=11)]
    name: Annotated[str, Field(description="nome do cliente", examples=["alexandre de carvalho pinto"], max_length=50)]
    password: Annotated[str, Field(description="senha do cliente", examples=["0123456789"], max_length=16)]


class ClientSchemaIn(ClientSchema):
    pass


class ClientSchemaOut(ClientSchema, BaseSchemaOut):
    pass
