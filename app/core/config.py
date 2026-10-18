from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # DATABASE (Points to local SSMS in your .env)
    DATABASE_URL: str

    # CLOUDINARY
    CLOUD_NAME: str
    API_KEY: str
    API_SECRET: str


settings = Settings()