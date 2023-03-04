from pydantic import BaseSettings


# import os
# import pprint
# pprint.pprint(list(os.environ))


class Settings(BaseSettings):
    server_host: str = "127.0.0.1"
    server_port: int = 8000

    db_host: str
    db_port: str
    db_name: str
    db_user: str
    db_password: str
    db_url: str

    paralleldots_api_key: str

    jwt_secret: str
    jwt_algorithm: str = 'HS256'
    jwt_expires_s: int = 6000


settings = Settings()
# print(settings)
