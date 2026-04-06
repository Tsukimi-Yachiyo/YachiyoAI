from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    # 模型
    MODEL_NAME: str
    COMPRESS_MODEL_NAME: str
    BASE_URL: str
    EMBEDDINGS_MODEL_NAME: str

    # 数据库
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int

    API_DEPOSITORY_DB_TABLE_NAME: str
    CONVERSATION_DB_TABLE_NAME: str
    LONG_TERM_DB_TABLE_NAME: str
    KNOWLEDGE_BASE_DB_TABLE_NAME: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8")

settings = Settings()