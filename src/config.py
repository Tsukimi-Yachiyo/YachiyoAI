from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    # 模型
    MODEL_NAME: str
    COMPRESS_MODEL_NAME: str
    BASE_URL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8")

settings = Settings()