import os

import logfire
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.core.config import settings
from backend.routers.ingestion_leads import main as ingestion_leads_main
from backend.routers.transformation import main as transformation_leads_main

app = FastAPI()

logfire.configure(token=os.environ["LOGFIRE_TOKEN"])
logfire.instrument_fastapi(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.FRONTEND_HOST,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingestion_leads_main.router, prefix=settings.API_V1_STR)
app.include_router(transformation_leads_main.router, prefix=settings.API_V1_STR)
