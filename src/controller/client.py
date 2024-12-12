from uuid import uuid4
from fastapi import APIRouter, Body
from datetime import datetime

from src.config.dependencies import DatabaseDependency
from src.schemas.client import ClientSchemaIn, ClientSchemaOut
from src.model.client import ClientModel

router = APIRouter(prefix="/client", tags=["client"])


@router.post("/create", 
             response_model=ClientSchemaOut)
async def create_client(
    db_session: DatabaseDependency,
    client_in: ClientSchemaIn = Body(...)
) -> ClientSchemaOut:
    client_out = ClientSchemaOut(id=uuid4(), created_at=datetime.now(), **client_in.model_dump())
    client_model = ClientModel(**client_out.model_dump())

    db_session.add(client_model)
    await db_session.commit()

    return client_out
