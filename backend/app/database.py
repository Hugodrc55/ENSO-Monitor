"""Connexion à PostgreSQL : URL de la base, moteur SQLAlchemy et classe de base des modèles.

Aucune connexion n'est ouverte quand ce module est importé. L'API ne l'importe
pas encore : elle démarre et répond à /api/v1/health même sans base de données.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import MetaData, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase

# Fichier .env à la racine du dépôt, exclu de Git (modèle : .env.example).
# Une variable déjà définie dans l'environnement reste prioritaire.
ENV_FILE = Path(__file__).resolve().parents[2] / ".env"

# Noms explicites et stables pour les clés et contraintes. Ils figurent dans la
# migration et dans les messages d'erreur de PostgreSQL, par exemple
# « uq_observation_climate_index_id_year_season » en cas de doublon.
NAMING_CONVENTION = {
    "pk": "pk_%(table_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "uq": "uq_%(table_name)s_%(column_0_N_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "ix": "ix_%(table_name)s_%(column_0_N_name)s",
}


class Base(DeclarativeBase):
    """Classe de base des modèles : leurs tables partagent ces métadonnées."""

    metadata = MetaData(naming_convention=NAMING_CONVENTION)


def read_setting(name: str) -> str | None:
    """Lire une variable d'environnement, en complétant par le fichier .env s'il existe."""
    load_dotenv(ENV_FILE)
    return os.environ.get(name) or None


def get_database_url() -> str:
    """Renvoyer DATABASE_URL, utilisée à la fois par SQLAlchemy et par Alembic."""
    url = read_setting("DATABASE_URL")
    if url is None:
        raise RuntimeError(
            "DATABASE_URL n'est pas définie : copier .env.example en .env à la racine "
            "du dépôt, ou définir la variable dans l'environnement."
        )
    return url


def create_db_engine(url: str | None = None) -> Engine:
    """Créer un moteur SQLAlchemy ; la connexion n'est ouverte qu'à la première requête."""
    return create_engine(url or get_database_url())
