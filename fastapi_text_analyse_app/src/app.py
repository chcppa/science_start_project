import uvicorn
from fastapi import FastAPI

from services.auth.api import router as auth_router
from services.query_history.api import router as query_router
from settings import settings

tags_metadata = [
    {
        'name': 'auth',
        'description': 'Authorization and registration',
    },
    {
        'name': 'analysis',
        'description': 'Text analysis',
    }
]

app = FastAPI(
    title='Text Analyzer',
    description='Analyse text by 3 modes',
    version='1.0.0',
    openapi_tags=tags_metadata,
)

app.include_router(query_router)
app.include_router(auth_router)


if __name__ == "__main__":
    uvicorn.run(
        'app:app',
        host=settings.server_host,
        port=settings.server_port,
        reload=True
    )
