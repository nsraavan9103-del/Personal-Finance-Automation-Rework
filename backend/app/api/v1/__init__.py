from app.api.v1 import categories, transactions, upload, documents
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(categories.router, prefix='/categories', tags=['categories'])
api_router.include_router(transactions.router, prefix='/transactions', tags=['transactions'])
api_router.include_router(upload.router, prefix='/upload', tags=['upload'])
api_router.include_router(documents.router, prefix='/documents', tags=['documents'])
