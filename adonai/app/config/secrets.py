from os import urandom


class SecretsConfig:
    SECRET_KEY = urandom(1024)

    JWT_ACCESS_LIFESPAN = {"hours": 24}
    JWT_REFRESH_LIFESPAN = {"days": 30}
    JWT_ALGORITHM = "HS512"
