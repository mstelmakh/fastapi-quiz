from pydantic import BaseSettings


class Settings(BaseSettings):
    debug: bool = True
    title: str = "FastAPI Quiz Application"

    api_prefix: str = "/api"

    allowed_hosts: list[str] = ["*"]

    server_host: str = '127.0.0.1'
    server_port: int = 8000

    database_url: str


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8',
)
