from pydantic import BaseSettings


class Settings(BaseSettings):
    log_level: str = "INFO"
    discord_bot_token: str

    class Config:
        env_file = '.env'
        case_sensitive = False


settings = Settings()
