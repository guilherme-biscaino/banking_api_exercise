from typing import Annotated
from pydantic import Field
from src.contrib.schemas import BaseSchema


class ClientSchema(BaseSchema):
    cpf: Annotated[str, Field(description="Cpf do usuário", examples="836651540060", max_length=11)]
    name: Annotated[str, Field(description="Nome do usuário", examples="Alexandre carvalho", max_length=50)]
    password: Annotated[str, Field(description="Senha do usuário", examples="8467953158", max_length=10)]
