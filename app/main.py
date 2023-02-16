from app.core import settings
from fastapi import FastAPI
from app.api.routers import main_router


app = FastAPI(title=settings.app_title,
              description=settings.app_description,
              )
app.include_router(main_router)
