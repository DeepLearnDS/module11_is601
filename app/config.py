from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/fastapi_db"
    
    class Config:
        env_file = ".env"

settings = Settings()
class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/fastapi_db"
    SECRET_KEY: str = "change-this-to-a-secure-random-secret"

    class Config:
        env_file = ".env"