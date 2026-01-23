from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # Database

    DATABASE_URL : str


    # JWT Access Token Settings

    JWT_SECRET_KEY : str
    JWT_ALGORITHM : str
    JWT_ACCESS_TOKEN_EXPIRES: int


    # JWT Refresh Token Settings

    JWT_REFRESH_SECRET_KEY : str
    JWT_REFRESH_ALGORITHM : str
    JWT_REFRESH_TOKEN_EXPIRES: int

    # Message Encrypting

    MESSAGE_SECRET_KEY : str


    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()