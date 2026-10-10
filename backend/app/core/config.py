from pydantic_settings import BaseSettings
from typing import List, Union
import ast


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://finance_user:finance_access@localhost:5432/finance_db"
    CORS_ORIGINS: Union[str, List[str]] = "http://localhost:5173"
    SECRET_KEY: str = "dev-secret-change-in-production"
    DEBUG: bool = True

    class Config:
        env_file = ".env"

    @property
    def cors_origins_list(self) -> List[str]:
        if isinstance(self.CORS_ORIGINS, str):
            # Try to parse as Python list first
            try:
                return ast.literal_eval(self.CORS_ORIGINS)
            except (ValueError, SyntaxError):
                # Treat as comma-separated string
                return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]
        return self.CORS_ORIGINS


settings = Settings()
