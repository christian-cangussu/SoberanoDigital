from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://radar:radar@db:5432/radar"
    placsp_atom_url: str = ""
    match_keywords: str = "ingenieria,mantenimiento,software,consultoria,automatizacion,datos"
    min_score: int = 20
    poll_minutes: int = 60

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def keywords(self) -> list[str]:
        return [x.strip().lower() for x in self.match_keywords.split(",") if x.strip()]

settings = Settings()
