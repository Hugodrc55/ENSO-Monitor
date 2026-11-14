"""Connexion à PostgreSQL : URL de la base, moteur SQLAlchemy et classe de base des modèles.

Aucune connexion n'est ouverte quand ce module est importé : l'API démarre et
répond à /api/v1/health même sans base de données. La connexion n'a lieu qu'à la
première requête qui interroge la base.
"""

import os
from collections.abc import Iterator
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import MetaData, create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session

# Fichier .env à la racine du dépôt, exclu de Git (modèle : .env.example).
# Une variable déjà définie dans l'environnement reste prioritaire.
ENV_FILE = Path(__file__).resolve().parents[2] / ".env"

# Attente maximale pour ouvrir une connexion à PostgreSQL.
CONNECT_TIMEOUT_SECONDS = 5

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
    """Créer un moteur SQLAlchemy ; la connexion n'est ouverte qu'à la première requête.

    pool_pre_ping vérifie qu'une connexion conservée est encore valide, par exemple
    après un redémarrage de PostgreSQL. connect_timeout limite l'attente si la base
    est injoignable : sans lui, une connexion vers un port fermé peut attendre
    environ deux minutes sous Windows avant d'échouer.
    """
    return create_engine(
        url or get_database_url(),
        pool_pre_ping=True,
        connect_args={"connect_timeout": CONNECT_TIMEOUT_SECONDS},
    )


@lru_cache(maxsize=1)
def get_engine() -> Engine:
    """Moteur partagé par l'API, créé à la première requête qui en a besoin."""
    return create_db_engine()


def get_session() -> Iterator[Session]:
    """Dépendance FastAPI : une session par requête, fermée à la fin de la requête."""
    with Session(get_engine()) as session:
        yield session
