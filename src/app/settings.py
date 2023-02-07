from pydantic import BaseSettings


class Settings(BaseSettings):
    debug: bool = True
    title: str = "FastAPI Quiz Application"

    api_prefix: str = "/api"

    allowed_hosts: list[str] = ["*"]

    server_host: str = '127.0.0.1'
    server_port: int = 8000

    postgres_user: str
    postgres_password: str
    postgres_server: str
    postgres_db: str

    jwt_secret: str
    jwt_algorithm: str = 'HS256'
    jwt_expires_s: int = 3600

    @property
    def database_url(self):
        user = self.postgres_user
        password = self.postgres_password
        server = self.postgres_server
        db = self.postgres_db
        return f"postgresql://{user}:{password}@{server}/{db}"


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8',
)
