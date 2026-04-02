from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DASHSCOPE_API_KEY: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    MODEL_NAME: str
    BASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()