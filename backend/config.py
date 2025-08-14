import os
from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

env_path = Path(__file__).parent / "../.env"


class ConfigBase(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_path, env_file_encoding="utf-8", extra="ignore")


class AppConfig(ConfigBase):
    SERVER_HOST: str
    PRODUCTION: bool = True
    NGINX_PORT: int = 8002


class DatabaseConfig(ConfigBase):
    model_config = SettingsConfigDict(env_prefix="DB_")
    HOST: str
    PORT: int
    NAME: str
    USER: str
    PASS: SecretStr

    PORT_TEST: str | None = None


class AuthConfig(ConfigBase):
    VERIFYING_KEY: SecretStr
    JWT_ALGORITHM: str = "HS256"


class MinioConfig(ConfigBase):
    MINIO_ENDPOINT: str
    MINIO_ROOT_USER: str
    MINIO_ROOT_PASSWORD: SecretStr
    MINIO_SECURE: bool


def get_remote_minio_url(
    production: bool, host: str, proxy_port: int, minio_endpoint: str
) -> str | None:
    """Returns the remote MinIO URL based on the current environment.

    This function determines which URL should be used for accessing the MinIO storage.

    During local development, the request can access the MinIO container directly.
    In production, the request to the container goes through Nginx.

    Args:
        production (bool): A flag indicating the application environment.
                          If True, the production URL is returned.
        host (str): Where machine is deployed
        proxy_port (int): nginx port.
        minio_endpoint (str): Minio url.

    Returns:
        str: The MinIO URL specific to the current environment.
    """
    if production:
        return f"{host}:{proxy_port}/minio-api"
    else:
        return minio_endpoint


def create_database_url(config: DatabaseConfig, test_port: bool = False) -> str | None:
    """Generates a database connection URL.

    Args:
        config (DatabaseConfig): An instance of the configuration class containing database connection information.
        test_port (bool): If True, the test port (PORT_TEST) is used.

    Returns:
        str | None: A URL for the database or None if the test port is not specified.
    """
    port = config.PORT_TEST if test_port and config.PORT_TEST is not None else config.PORT
    if port is None:
        return None

    return f"postgresql+asyncpg://{config.USER}:{config.PASS.get_secret_value()}@{config.HOST}:{port}/{config.NAME}"


db_conf = DatabaseConfig()
auth_config = AuthConfig()
minio_config = MinioConfig()
app_config = AppConfig()
REMOTE_MINIO_URL = get_remote_minio_url(
    app_config.PRODUCTION,
    app_config.SERVER_HOST,
    app_config.NGINX_PORT,
    minio_config.MINIO_ENDPOINT,
)
DATABASE_URL = create_database_url(db_conf)
DATABASE_URL_TEST = create_database_url(db_conf, test_port=True)
TEMP_FOLDER = "./temp"

os.makedirs(TEMP_FOLDER, exist_ok=True)
