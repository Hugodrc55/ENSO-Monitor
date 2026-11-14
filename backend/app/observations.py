"""Consultation des observations ONI : GET /api/v1/observations?start=…&end=…"""

from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_session
from app.models import ClimateIndex, Observation

# Série servie par l'API : une seule pour ce MVP.
SERIES_CODE = "ONI_ERSSTv6"

router = APIRouter(prefix="/api/v1", tags=["observations"])


class SeriesInfo(BaseModel):
    """Série et provenance, à afficher avec les valeurs."""

    code: str = Field(examples=["ONI_ERSSTv6"])
    name: str = Field(examples=["Oceanic Niño Index (ONI)"])
    version: str = Field(description="Version vérifiée de la série")
    unit: str = Field(description="Unité des valeurs", examples=["°C"])
    source: str = Field(description="Producteur des données")


class ObservationOut(BaseModel):
    reference_month: date = Field(
        description="Date de référence : 1er jour du mois central de la saison. "
        "C'est une convention de date ; la valeur couvre trois mois.",
        examples=["2015-12-01"],
    )
    season: str = Field(description="Saison NOAA d'origine (SEAS)", examples=["NDJ"])
    year: int = Field(
        description="Année NOAA d'origine (YR), celle du mois central", examples=[2015]
    )
    oni: float = Field(
        description="Valeur ONI en °C : colonne ANOM du fichier NOAA, deux décimales",
        examples=[2.59],
    )


class ObservationsResponse(BaseModel):
    series: SeriesInfo
    start: date = Field(description="Début de la période demandée (inclus)")
    end: date = Field(description="Fin de la période demandée (incluse)")
    observations: list[ObservationOut] = Field(
        description="Observations dont la date de référence est comprise entre start et "
        "end, bornes incluses, dans l'ordre chronologique. Liste vide si la période "
        "n'en contient aucune."
    )


StartQuery = Annotated[
    date,
    Query(
        description="Début de la période, **inclus**, au format AAAA-MM-JJ. "
        "Comparé à la date de référence de chaque saison.",
        examples=["2015-01-01"],
    ),
]
EndQuery = Annotated[
    date,
    Query(
        description="Fin de la période, **incluse**, au format AAAA-MM-JJ. "
        "Ne doit pas précéder le début.",
        examples=["2016-12-31"],
    ),
]


@router.get(
    "/observations",
    summary="Observations ONI d'une période",
    responses={
        404: {"description": "Série absente : observations pas encore importées"},
        422: {"description": "Date invalide ou manquante, ou début postérieur à la fin"},
        503: {"description": "Base de données indisponible"},
    },
)
def list_observations(
    start: StartQuery,
    end: EndQuery,
    session: Annotated[Session, Depends(get_session)],
) -> ObservationsResponse:
    """Renvoyer les observations ONI ERSSTv6 dont la date de référence est dans [start, end]."""
    if start > end:
        raise HTTPException(
            status_code=422,
            detail=f"La date de début ({start}) est postérieure à la date de fin ({end}).",
        )

    index = session.scalar(select(ClimateIndex).where(ClimateIndex.code == SERIES_CODE))
    if index is None:
        raise HTTPException(
            status_code=404,
            detail=f"Série {SERIES_CODE} absente de la base : importer les observations.",
        )

    rows = session.scalars(
        select(Observation)
        .where(
            Observation.climate_index_id == index.id,
            Observation.reference_month >= start,  # bornes incluses
            Observation.reference_month <= end,
        )
        .order_by(Observation.reference_month)
    ).all()

    return ObservationsResponse(
        series=SeriesInfo(
            code=index.code,
            name=index.name,
            version=index.version,
            unit=index.unit,
            source=index.source.name,
        ),
        start=start,
        end=end,
        observations=[
            # NUMERIC → float : la valeur garde ses deux décimales dans le JSON (ex. 2.59).
            ObservationOut(reference_month=row.reference_month, season=row.season,
                           year=row.year, oni=float(row.anom_c))
            for row in rows
        ],
    )
