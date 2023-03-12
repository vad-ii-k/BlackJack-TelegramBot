import typing
from dataclasses import dataclass

from environs import Env

if typing.TYPE_CHECKING:
    from app.web.app import Application


@dataclass
class SessionConfig:
    key: str


@dataclass
class BotConfig:
    token: str
    name: str


@dataclass
class DatabaseConfig:
    host: str
    port: int
    user: str
    password: str
    database: str

    @property
    def connection_url(self) -> str:
        return (
            f"postgresql+asyncpg://"
            f"{self.user}:{self.password}@{self.host}:{self.port}"
            f"/{self.database}"
        )


@dataclass
class Config:
    session: SessionConfig = None
    bot: BotConfig = None
    database: DatabaseConfig = None


def setup_config(app: "Application", env_path: str):
    env = Env()
    env.read_env(env_path)

    app.config = Config(
        session=SessionConfig(key=env.str("SESSION_KEY")),
        bot=BotConfig(token=env.str("BOT_TOKEN"), name=env.str("BOT_NAME")),
        database=DatabaseConfig(
            host=env.str("DB_HOST"),
            port=env.int("DB_PORT"),
            user=env.str("DB_USER"),
            password=env.str("DB_PASSWORD"),
            database=env.str("DB_NAME"),
        ),
    )
