from fastapi import FastAPI
from src.controller import client, account, transaction, auth


app = FastAPI(title="banking api test")
app.include_router(client.router)
app.include_router(account.router)
app.include_router(transaction.router)
app.include_router(auth.router)
