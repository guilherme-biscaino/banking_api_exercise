from pydantic import BaseModel, UUID4, Field
from typing import Annotated
from datetime import datetime


class BaseSchema(BaseModel):
    class Config:
        extra = 'forbid'
        from_attributes = True


class BaseSchemaOut(BaseSchema):
    id: Annotated[UUID4, Field(description="Identifier")]
    created_at: Annotated[datetime, Field(description="creation date")]