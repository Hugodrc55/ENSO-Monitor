"""Point d'entrée de l'API : santé du service et consultation des observations ONI."""

import logging
from typing import Literal

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy.exc import OperationalError

from app import observations

logger = logging.getLogger(__name__)

app = FastAPI(
    title="ENSO Monitor API",
    version="0.2.0",
    description="API du projet individuel ENSO Monitor : observations NOAA ONI ERSSTv6 "
    "importées dans PostgreSQL.",
)
app.include_router(observations.router)


@app.exception_handler(OperationalError)
def database_unavailable(request: Request, error: OperationalError) -> JSONResponse:
    """Base injoignable : réponse 503 explicite au lieu d'une erreur 500."""
    logger.warning("Base de données indisponible pendant %s : %s", request.url.path, error)
    return JSONResponse(status_code=503, content={"detail": "Base de données indisponible."})


class HealthResponse(BaseModel):
    """Contrat de réponse : disponibilité HTTP, sans vérification de base de données."""

    status: Literal["ok"]
    service: str


@app.get("/api/v1/health", response_model=HealthResponse, tags=["health"])
def health() -> HealthResponse:
    """Indiquer que l'API répond. Aucune donnée scientifique n'est interrogée."""
    return HealthResponse(status="ok", service="enso-monitor-api")
