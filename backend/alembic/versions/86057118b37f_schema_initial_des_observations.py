"""Schéma initial : source, climate_index, data_import et observation.

Générée par `alembic revision --autogenerate` à partir de app/models.py, puis
relue : ordre de création, clés, contraintes d'unicité et de contrôle, index.
Aucune donnée n'est insérée par cette migration.

Revision ID: 86057118b37f
Revises:
Create Date: 2026-11-14 01:47:00.804634

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '86057118b37f'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Opérations générées par Alembic, relues avant application.
    op.create_table('source',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=32), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('url', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_source')),
    sa.UniqueConstraint('code', name=op.f('uq_source_code'))
    )
    op.create_table('climate_index',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('source_id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=32), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('version', sa.String(length=100), nullable=False),
    sa.Column('unit', sa.String(length=16), nullable=False),
    sa.Column('reference_url', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['source_id'], ['source.id'], name=op.f('fk_climate_index_source_id_source')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_climate_index')),
    sa.UniqueConstraint('code', name=op.f('uq_climate_index_code'))
    )
    op.create_table('data_import',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('climate_index_id', sa.Integer(), nullable=False),
    sa.Column('file_name', sa.String(length=255), nullable=False),
    sa.Column('source_url', sa.Text(), nullable=False),
    sa.Column('sha256', sa.String(length=64), nullable=False),
    sa.Column('downloaded_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('source_last_modified', sa.DateTime(timezone=True), nullable=True),
    sa.Column('version_evidence', sa.Text(), nullable=False),
    sa.Column('imported_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.CheckConstraint("sha256 ~ '^[0-9a-f]{64}$'", name=op.f('ck_data_import_sha256_hex')),
    sa.CheckConstraint('imported_at >= downloaded_at', name=op.f('ck_data_import_imported_after_download')),
    sa.ForeignKeyConstraint(['climate_index_id'], ['climate_index.id'], name=op.f('fk_data_import_climate_index_id_climate_index')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_data_import')),
    sa.UniqueConstraint('id', 'climate_index_id', name=op.f('uq_data_import_id_climate_index_id')),
    sa.UniqueConstraint('sha256', name=op.f('uq_data_import_sha256'))
    )
    op.create_table('observation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('climate_index_id', sa.Integer(), nullable=False),
    sa.Column('data_import_id', sa.Integer(), nullable=False),
    sa.Column('reference_month', sa.Date(), nullable=False),
    sa.Column('season', sa.String(length=3), nullable=False),
    sa.Column('year', sa.SmallInteger(), nullable=False),
    sa.Column('total_c', sa.Numeric(precision=4, scale=2), nullable=False),
    sa.Column('anom_c', sa.Numeric(precision=4, scale=2), nullable=False),
    sa.Column('source_line', sa.Integer(), nullable=False),
    sa.CheckConstraint("reference_month = make_date(year, array_position(ARRAY['DJF', 'JFM', 'FMA', 'MAM', 'AMJ', 'MJJ', 'JJA', 'JAS', 'ASO', 'SON', 'OND', 'NDJ']::text[], season::text), 1)", name=op.f('ck_observation_reference_month_central')),
    sa.CheckConstraint("season IN ('DJF', 'JFM', 'FMA', 'MAM', 'AMJ', 'MJJ', 'JJA', 'JAS', 'ASO', 'SON', 'OND', 'NDJ')", name=op.f('ck_observation_season_code')),
    sa.CheckConstraint('anom_c BETWEEN -10 AND 10', name=op.f('ck_observation_anom_physical_range')),
    sa.CheckConstraint('source_line > 1', name=op.f('ck_observation_source_line_after_header')),
    sa.CheckConstraint('total_c BETWEEN -2 AND 40', name=op.f('ck_observation_total_physical_range')),
    sa.CheckConstraint('year >= 1950', name=op.f('ck_observation_year_min')),
    sa.ForeignKeyConstraint(['climate_index_id'], ['climate_index.id'], name=op.f('fk_observation_climate_index_id_climate_index')),
    sa.ForeignKeyConstraint(['data_import_id', 'climate_index_id'], ['data_import.id', 'data_import.climate_index_id'], name=op.f('fk_observation_data_import_id_data_import')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_observation')),
    sa.UniqueConstraint('climate_index_id', 'year', 'season', name=op.f('uq_observation_climate_index_id_year_season'))
    )
    op.create_index('ix_observation_climate_index_id_reference_month', 'observation', ['climate_index_id', 'reference_month'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    # Opérations générées par Alembic, relues avant application.
    op.drop_index('ix_observation_climate_index_id_reference_month', table_name='observation')
    op.drop_table('observation')
    op.drop_table('data_import')
    op.drop_table('climate_index')
    op.drop_table('source')
