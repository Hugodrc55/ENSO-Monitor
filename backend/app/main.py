"""Point d'entrée de l'API, limité à la santé du service au Jour 1."""

from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(
    title="ENSO Monitor API",
    version="0.1.0",
    description="API du projet individuel ENSO Monitor. Initialisation au Jour 1.",
)


class HealthResponse(BaseModel):
    """Contrat de réponse : disponibilité HTTP, sans vérification de base de données."""

    status: Literal["ok"]
    service: str


@app.get("/api/v1/health", response_model=HealthResponse, tags=["health"])
def health() -> HealthResponse:
    """Indiquer que l'API répond. Aucune donnée scientifique n'est interrogée."""
    return HealthResponse(status="ok", service="enso-monitor-api")
