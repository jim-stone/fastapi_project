from pydantic import BaseSettings


class Settings(BaseSettings):
    database_name: str = 'fastapi'
    database_hostname: str = 'localhost'
    database_port: str = '5432'
    database_password: str = 'coderslab'
    database_username: str = 'postgres'

    class Config:
        env_file = '.env'


settings = Settings()
print(settings)
