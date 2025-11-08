# app/core/settings.py
import json
import os
from pydash import py_
from functools import lru_cache, partial
from pydantic import ConfigDict
from pydantic_settings import BaseSettings

CONFIG_FILE_NAMES = ["env-config.json"]

class PostgresSettings(BaseSettings):
    """
    Postgres Settings
    """

    pg_db: str = os.getenv("POSTGRES_DB", "postgres")
    pg_user: str = os.getenv("POSTGRES_USER", "test1")
    pg_password: str = os.getenv("POSTGRES_PASSWORD", "test1")
    pg_port: int = 5432
    pg_host: str = os.getenv("POSTGRES_HOST", "")

    @property
    def pg_dsn(self: "PostgresSettings") -> str:
        """Returns Postgres DSN"""
        return f"postgresql://{self.pg_user}:{self.pg_password}@{self.pg_host}:{self.pg_port}/{self.pg_db}"



class AppSettings(BaseSettings):
    """Default settings"""
    model_config = ConfigDict(extra="ignore")
    api_prefix: str = "/api/v1"
    
    
    # Postgres settings
    postgres: PostgresSettings = PostgresSettings()

    
    

@lru_cache
def get_settings():
    """
    Load settings from config files and environment variables.
    """
    settings: AppSettings =  AppSettings()
    

    config_dir = os.getenv("APP_CONFIG_DIR", "/")

    # Load and merge any existing config files
    combined_config = dict()
    for file in CONFIG_FILE_NAMES:
        config_path = os.path.join(config_dir, file)
        if os.path.exists(config_path):
            with open(config_path) as f:
                combined_config.update(json.loads(f.read()))

    # Only update settings if we found valid config files
    if combined_config:
        default_settings_dict = settings.model_dump()
        default_settings_dict_partial = partial(py_.set_, default_settings_dict)

        for key, val in combined_config.items():
            default_settings_dict_partial(key, val)

        settings = settings.model_validate(default_settings_dict)
    
    return settings