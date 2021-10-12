import os
from dataclasses import dataclass

import yaml
from marshmallow import Schema, fields, post_load

DEFAULT_CONFIG_PATH = os.getenv('MOVIE_CFG', './data/movie_app.yaml')


class DBConfigSchema(Schema):
    port = fields.Integer(required=True)
    host = fields.String(required=True)
    name = fields.String(required=True)
    user = fields.String(required=True)
    password = fields.String(required=True)

    @post_load
    def make_config(self, data, **kwargs):
        return DbConfig(**data)


class MovieAppConfigSchema(Schema):
    logging = fields.String(required=False, missing='enabled')
    log_level = fields.Integer(required=False, missing=3)
    logfile = fields.String(required=False, missing='enabled')
    data_url = fields.String(required=True)

    @post_load
    def make_config(self, data, **kwargs):
        return MovieAppConfig(**data)


class ConfigSchema(Schema):
    db = fields.Nested(DBConfigSchema)
    movie_app = fields.Nested(MovieAppConfigSchema)

    @post_load
    def make_config(self, data, **kwargs):
        return AppConfig(**data)


@dataclass
class DbConfig:
    port: int
    host: str
    name: str
    user: str
    password: str


@dataclass
class MovieAppConfig:
    logging: bool
    log_level: int
    logfile: str
    data_url: str


@dataclass
class AppConfig:
    db: DbConfig
    movie_app: MovieAppConfig

    @classmethod
    def load_config(cls, path: str ) -> 'AppConfig':
        with open(path, 'r') as file_:
            config_dict: dict = yaml.safe_load(file_)
        return ConfigSchema().load(config_dict)

    @property
    def pg_conn_dsn(self) -> str:
        return f"{self.db.user}:{self.db.password}@{self.db.host}:{self.db.port}/{self.db.name}"

    @property
    def db_url(self) -> str:
        return f"postgresql+psycopg2://{self.pg_conn_dsn}"

    def is_logging_enabled(self):
        return True if self.movie_app.logging== 'enabled' else False


app_config = AppConfig.load_config(DEFAULT_CONFIG_PATH)