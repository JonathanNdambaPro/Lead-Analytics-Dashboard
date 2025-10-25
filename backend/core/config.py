from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_DIR = Path(__file__).parents[2]
ENV_FILE = ROOT_DIR / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE, env_file_encoding="utf-8")

    NOTION_TOKEN: str
    DATABASE_ID: str

    API_V1_STR: str = "/api/v1"
    FRONTEND_HOST: list[str] = ["http://localhost:3000", "http://localhost:3001"]
    PATH_DELTALAKE: Path = Path(__file__).parents[1] / "data_leads"


settings = Settings()
