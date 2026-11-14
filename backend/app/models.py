"""Modèle de données : Source → ClimateIndex → DataImport → Observation.

- Une source (producteur, ex. NOAA CPC) publie plusieurs indices.
- Un indice (série dans une version confirmée, ex. ONI ERSSTv6) reçoit plusieurs imports.
- Un import (un fichier brut chargé) produit plusieurs observations.
- Une observation (une saison NOAA) est reliée à l'import qui l'a chargée, et par
  lui au fichier d'origine, à l'indice et à la source.

Les noms de tables et de colonnes sont en anglais, comme le code. Correspondance
avec les entités du dossier : Source = source, Indice = climate_index,
Import = data_import, Observation = observation.
"""

from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    Numeric,
    SmallInteger,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

# Codes NOAA dans l'ordre de leur mois central : DJF → janvier, ..., NDJ → décembre.
# Même liste et même ordre que SEASONS dans etl/transform_oni.py.
NOAA_SEASONS = ("DJF", "JFM", "FMA", "MAM", "AMJ", "MJJ", "JJA", "JAS", "ASO", "SON", "OND", "NDJ")
SEASONS_SQL = ", ".join(f"'{season}'" for season in NOAA_SEASONS)

FIRST_YEAR = 1950  # première année de la série ONI


class Source(Base):
    """Producteur des données, par exemple le Climate Prediction Center de la NOAA."""

    __tablename__ = "source"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(32), unique=True)  # ex. NOAA_CPC
    name: Mapped[str] = mapped_column(String(200))
    url: Mapped[str] = mapped_column(Text)

    climate_indices: Mapped[list["ClimateIndex"]] = relationship(back_populates="source")


class ClimateIndex(Base):
    """Série d'indice publiée par une source, dans une version confirmée."""

    __tablename__ = "climate_index"

    id: Mapped[int] = mapped_column(primary_key=True)
    source_id: Mapped[int] = mapped_column(ForeignKey("source.id"))
    code: Mapped[str] = mapped_column(String(32), unique=True)  # ex. ONI_ERSSTv6
    name: Mapped[str] = mapped_column(String(200))  # ex. Oceanic Niño Index
    # Version confirmée de la série, ex. « ERSSTv6, périodes de base centrées ».
    version: Mapped[str] = mapped_column(String(100))
    unit: Mapped[str] = mapped_column(String(16))  # ex. °C
    reference_url: Mapped[str] = mapped_column(Text)  # page de documentation NOAA

    source: Mapped[Source] = relationship(back_populates="climate_indices")
    imports: Mapped[list["DataImport"]] = relationship(back_populates="climate_index")


class DataImport(Base):
    """Chargement d'un fichier brut : provenance du fichier et date du chargement en base.

    Un fichier n'est rattaché à un indice qu'une fois sa version confirmée ;
    version_evidence indique comment elle l'a été.
    """

    __tablename__ = "data_import"
    __table_args__ = (
        # Redondant avec la clé primaire, mais nécessaire comme cible de la clé
        # étrangère composite d'Observation (cohérence entre indice et import).
        UniqueConstraint("id", "climate_index_id"),
        CheckConstraint("sha256 ~ '^[0-9a-f]{64}$'", name="sha256_hex"),
        CheckConstraint("imported_at >= downloaded_at", name="imported_after_download"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    climate_index_id: Mapped[int] = mapped_column(ForeignKey("climate_index.id"))
    file_name: Mapped[str] = mapped_column(String(255))  # nom dans data/raw/
    source_url: Mapped[str] = mapped_column(Text)  # URL exacte du téléchargement
    # Un même fichier (mêmes octets) n'est enregistré qu'une fois.
    sha256: Mapped[str] = mapped_column(String(64), unique=True)
    # Date d'extraction : téléchargement du fichier auprès de la NOAA.
    downloaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    # En-tête Last-Modified du serveur NOAA, s'il a été fourni.
    source_last_modified: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    version_evidence: Mapped[str] = mapped_column(Text)
    # Date du chargement en base, distincte de la date d'extraction.
    imported_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    climate_index: Mapped[ClimateIndex] = relationship(back_populates="imports")
    observations: Mapped[list["Observation"]] = relationship(back_populates="data_import")


class Observation(Base):
    """Valeur d'une saison NOAA, telle que publiée, avec sa date de référence."""

    __tablename__ = "observation"
    __table_args__ = (
        # Une seule valeur par saison et par série, quel que soit l'import :
        # data_import_id ne fait volontairement pas partie de la contrainte.
        UniqueConstraint("climate_index_id", "year", "season"),
        # L'indice de l'observation doit être celui de son import.
        ForeignKeyConstraint(
            ["data_import_id", "climate_index_id"],
            ["data_import.id", "data_import.climate_index_id"],
        ),
        CheckConstraint(f"season IN ({SEASONS_SQL})", name="season_code"),
        CheckConstraint(f"year >= {FIRST_YEAR}", name="year_min"),
        # Règle de datation : 1er jour du mois central, dans l'année YR.
        # array_position donne le rang de la saison (1 pour DJF, ..., 12 pour NDJ).
        CheckConstraint(
            "reference_month = "
            f"make_date(year, array_position(ARRAY[{SEASONS_SQL}]::text[], season::text), 1)",
            name="reference_month_central",
        ),
        # Bornes physiques larges, identiques à celles de la transformation.
        CheckConstraint("total_c BETWEEN -2 AND 40", name="total_physical_range"),
        CheckConstraint("anom_c BETWEEN -10 AND 10", name="anom_physical_range"),
        CheckConstraint("source_line > 1", name="source_line_after_header"),
        # Futur filtre par période : une série, entre deux dates, triée par date.
        Index(
            "ix_observation_climate_index_id_reference_month",
            "climate_index_id",
            "reference_month",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    climate_index_id: Mapped[int] = mapped_column(ForeignKey("climate_index.id"))
    data_import_id: Mapped[int]
    # Date de référence au format SQL DATE (convention, pas une mesure ce jour-là).
    reference_month: Mapped[date] = mapped_column(Date)
    season: Mapped[str] = mapped_column(String(3))  # SEAS d'origine
    year: Mapped[int] = mapped_column(SmallInteger)  # YR d'origine
    # NUMERIC(4, 2) : valeurs exactes à deux décimales, comme dans le fichier NOAA.
    total_c: Mapped[Decimal] = mapped_column(Numeric(4, 2))  # TOTAL, °C
    anom_c: Mapped[Decimal] = mapped_column(Numeric(4, 2))  # ANOM, °C : valeur de l'ONI
    source_line: Mapped[int]  # ligne dans le fichier brut de l'import

    data_import: Mapped[DataImport] = relationship(back_populates="observations")
