"""Fixtures partagées : base PostgreSQL jetable, créée par la migration Alembic.

La base est désignée par TEST_DATABASE_URL (nom terminé par « _test ») et vidée
avant et après la série de tests. Sans cette variable, les tests qui en ont besoin
sont ignorés. Chaque test travaille dans une transaction annulée à la fin : aucune
donnée n'est conservée d'un test à l'autre.
"""

from collections.abc import Iterator
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import Engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session

from app.database import create_db_engine, read_setting

ALEMBIC_INI = Path(__file__).resolve().parents[1] / "alembic.ini"


@pytest.fixture(scope="session")
def alembic_config() -> Config:
    url = read_setting("TEST_DATABASE_URL")
    if url is None:
        pytest.skip("TEST_DATABASE_URL non définie : pas de base de test")
    if not make_url(url).database.endswith("_test"):
        pytest.fail("TEST_DATABASE_URL doit désigner une base jetable, nommée en _test")
    config = Config(str(ALEMBIC_INI))
    config.attributes["database_url"] = url
    return config


@pytest.fixture(scope="session")
def engine(alembic_config: Config) -> Iterator[Engine]:
    """Schéma créé par la migration (et non par create_all), puis supprimé à la fin."""
    command.downgrade(alembic_config, "base")
    command.upgrade(alembic_config, "head")
    engine = create_db_engine(alembic_config.attributes["database_url"])
    yield engine
    engine.dispose()
    command.downgrade(alembic_config, "base")


@pytest.fixture
def session(engine: Engine) -> Iterator[Session]:
    """Session dans une transaction annulée à la fin du test.

    Un commit éventuel du code testé ne valide qu'un point de sauvegarde interne
    (join_transaction_mode) : la transaction englobante reste annulée.
    """
    with engine.connect() as connection:
        transaction = connection.begin()
        session = Session(bind=connection, join_transaction_mode="create_savepoint")
        try:
            yield session
        finally:
            session.close()
            transaction.rollback()
