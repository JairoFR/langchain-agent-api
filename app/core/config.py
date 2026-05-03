# pydantic-settings lee variables de entorno o del archivo .env
# y las expone como atributos tipados. Centraliza toda la configuración.
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    GROQ_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()