"""Environnement d'Alembic : migrations du schéma décrit dans app.models.

L'URL vient de DATABASE_URL (variable d'environnement ou fichier .env à la
racine), comme pour SQLAlchemy. Un appel depuis Python peut fournir une autre URL
dans config.attributes["database_url"] : les tests du schéma l'utilisent pour
travailler sur une base jetable.
"""

from logging.config import fileConfig

from alembic import context
from sqlalchemy import create_engine, pool

from app import models  # noqa: F401  (déclare les tables dans Base.metadata)
from app.database import Base, get_database_url

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name, disable_existing_loggers=False)

# Métadonnées des modèles : point de comparaison pour `alembic revision --autogenerate`.
target_metadata = Base.metadata


def database_url() -> str:
    return config.attributes.get("database_url") or get_database_url()


def run_migrations_offline() -> None:
    """Écrire le SQL des migrations sans se connecter (`alembic upgrade head --sql`)."""
    context.configure(
        url=database_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Appliquer les migrations sur la base, dans une transaction."""
    engine = create_engine(database_url(), poolclass=pool.NullPool)
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
