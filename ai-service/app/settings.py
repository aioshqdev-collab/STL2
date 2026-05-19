from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    service_name: str = "STLForge AI"
    device: str = "cuda"
    model_provider: str = "mock"
    public_base_url: str = "http://127.0.0.1:8100"
    work_dir: Path = Path("./work")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="AI_",
        extra="ignore",
    )


settings = Settings()
