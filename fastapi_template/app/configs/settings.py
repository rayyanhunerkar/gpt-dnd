from pathlib import Path

from envyaml import EnvYAML

BASE_DIR = Path(__name__).resolve().parent
env = EnvYAML(f'{BASE_DIR}/fastapi_template/app/configs/env.yaml')


class ProjectSettings:
    title: str = env['project.title']
    host: str = env['project.host']
    port: int = env['project.port']
    root_path = env['project.root-path']
    version: str = env['project.version']
    debug: bool = env['project.debug']


class DBSettings:
    host: str = env['database.host']
    port: int = env['database.port']
    username: str = env['database.username']
    password: str = env['database.password']
    name: str = env['database.name']
    schema: str = env['database.schema']
    config: str = f"postgresql+asyncpg://{username}:{password}@{host}/{name}"
    config_test: str = f"postgresql+asyncpg://{username}:{password}@{host}/test"


class JWTSettings:
    secret_key: str = env['auth.secret-key']
    algo: str = env['auth.algorithm']
