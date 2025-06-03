from fastapi import APIRouter
from app.api.endpoints import user as user_router
from app.api.endpoints import rag as rag_router
from app.api.endpoints import authentication as auth_router

router = APIRouter()

# Include authentication-related routes
router.include_router(auth_router.router, tags=['AUTHENTICATION V1'], prefix='/api/v1/authentication')


# Include user-related routes under the /api/v1 prefix and tag them as 'USER V1'
router.include_router(user_router.router, tags=['USER V1'], prefix='/api/v1/users')

# Include RAG-related routes under the /api/v1 prefix and tag them as 'RAG V1'
router.include_router(rag_router.router, tags=['RAG V1'], prefix='/api/v1/rag')