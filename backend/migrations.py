from alembic import command
from alembic.config import Config
from config import DATABASE_URL


def run_migrations(script_location: str, dsn: str) -> None:
    alembic_cfg = Config()
    alembic_cfg.set_main_option("script_location", script_location)
    alembic_cfg.set_main_option("sqlalchemy.url", dsn)
    command.upgrade(alembic_cfg, "head")


run_migrations("alembic", DATABASE_URL)
