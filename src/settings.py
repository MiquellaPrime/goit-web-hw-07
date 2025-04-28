from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseSettingsWithConfig(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


class DBSettings(BaseSettingsWithConfig):
    model_config = SettingsConfigDict(env_prefix="db_")

    host:   str
    port:   int
    user:   str
    passwd: str
    name:   str

    @property
    def postgres_dsn(self) -> str:
        return f"postgresql://{self.user}:{self.passwd}@{self.host}:{self.port}/{self.name}"


class Settings(BaseSettingsWithConfig):
    IS_DEV: bool = Field(False, alias="development")

    db: DBSettings = DBSettings()


settings = Settings()
