from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'QRKot'
    app_description: str = 'Проект для сбора пожертвований'
    database_url: str = 'sqlite+aiosqlite:///./qrkot.db'
    secret: str = 'hb1i2b4i1hj1jh24vb'

    class Config:
        env_file = '.env'


settings = Settings()
