import secrets
from pathlib import Path

from pydantic import AnyHttpUrl, EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env")

    API_V1_STR: str = "/api"
    SECRET_KEY: str = secrets.token_urlsafe(32)

    ACCESS_TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24
    JWT_ALGO: str = "HS512"

    EMAIL_TEST_USER: EmailStr = "test@example.com"
    FIRST_SUPERUSER: EmailStr
    FIRST_SUPERUSER_PASSWORD: str

    MONGO_DATABASE: str = ""
    MONGO_DATABASE_URI: str = ""

    MULTI_MAX: int = 10

    BASE_DIR: Path = BASE_DIR

    # stripe

    STRIPE_API_KEY: str
    STRIPE_WEBHOOK_SECRET: str = secrets.token_urlsafe(32)
    STRIPE_SUCCESS_URL: AnyHttpUrl = "http://localhost:8000/docs"
    STRIPE_CANCEL_URL: AnyHttpUrl = "http://localhost:8000/docs"

    HOST_URL: Path = "http://localhost:8000"

    # firebase

    FIREBASE_STORAGE_BUCKET: str
    FIREBASE_TYPE: str
    FIREBASE_PROJECT_ID: str
    FIREBASE_PRIVATE_KEY_ID: str
    FIREBASE_PRIVATE_KEY: str
    FIREBASE_CLIENT_EMAIL: str
    FIREBASE_CLIENT_ID: str
    FIREBASE_AUTH_URI: str
    FIREBASE_TOKEN_URI: str
    FIREBASE_AUTH_PROVIDER_X509_CERT_URL: str
    FIREBASE_CLIENT_X509_CERT_URL: str
    FIREBASE_UNIVERSE_DOMAIN: str


settings = Settings()

hhh = "sdfs\n"
