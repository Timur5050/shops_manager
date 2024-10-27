from pathlib import Path

from pydantic.v1 import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent


class AuthJWT(BaseSettings):
    private_key_path: Path = BASE_DIR / "shop_manager" / "certs" / "private.pem"
    public_key_path: Path = BASE_DIR / "shop_manager" / "certs" / "public.pem"
    algorithm: str = "RS256"
    access_token_exp_minutes: int = 15
    refresh_token_exp_minutes: int = 60 * 24


class Settings(BaseSettings):
    PROJECT_NAME: str = "Expense Tracker"

    DATABASE_URL: str | None = "sqlite:///./shops_manager.sqlite3"
    ASYNC_DATABASE_URL: str | None = "sqlite+aiosqlite:///./shops_manager.sqlite3"
    auth_jwt: AuthJWT = AuthJWT()

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
