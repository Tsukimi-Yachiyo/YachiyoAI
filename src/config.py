from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # 阿里云百炼
    DASHSCOPE_API_KEY: str
    # PostgresSQL
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    # 模型
    MODEL_NAME: str
    BASE_URL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8")

settings = Settings()