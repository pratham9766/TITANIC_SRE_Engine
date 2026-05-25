from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    openai_api_key: str | None = None
    openai_model: str = "gpt-4.1"
    jwt_secret: str = "change_me_for_local_demo"
    jwt_issuer: str = "titanic-api"
    cors_origins: str = "http://localhost:4173,http://127.0.0.1:4173,http://localhost:5173,http://127.0.0.1:5173"
    database_url: str = "postgresql+psycopg://titanic:titanic@localhost:5432/titanic"
    redis_url: str = "redis://localhost:6379/0"
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = "change_me"
    qdrant_url: str = "http://localhost:6333"
    qdrant_api_key: str | None = None
    prometheus_url: str = "http://localhost:9090"
    grafana_url: str | None = None
    grafana_api_key: str | None = None
    datadog_api_key: str | None = None
    datadog_app_key: str | None = None
    otel_exporter_otlp_endpoint: str = "http://localhost:4317"
    autonomy_mode: str = "recommend_only"
    require_human_approval: bool = True
    allow_production_writes: bool = False
    recovery_dry_run: bool = True


settings = Settings()


def cors_origin_list() -> list[str]:
    return [origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()]
