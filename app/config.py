from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file='.env') #This retrive values from the .env file


settings = Settings()