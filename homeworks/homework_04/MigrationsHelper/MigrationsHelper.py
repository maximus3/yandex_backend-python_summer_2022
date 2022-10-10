import os
import subprocess
from types import SimpleNamespace

from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine

from config.config import BASE_DIR

if "GITLAB_RUN" in os.environ.keys():
    db_host = "postgres"
else:
    db_host = "localhost"

db_string = "postgresql://%s:%s@%s:%s/%s" % (
    os.environ["POSTGRES_USER"],
    os.environ["POSTGRES_PASSWORD"],
    db_host,
    "5432",
    os.environ["POSTGRES_DB"],
)
db = create_engine(db_string)


def update(migrations_count):
    if os.environ["SDB_TRACK"] == "java":
        update_java(str(migrations_count))
    else:
        update_python(str(migrations_count))


def rollback(migrations_count):
    if os.environ["SDB_TRACK"] == "java":
        rollback_java(str(migrations_count))
    else:
        rollback_python(str(migrations_count))


def make_alembic_config():
    base_path = BASE_DIR
    cmd_opts = SimpleNamespace(config="migrations/python/", pg_url=db_string, name="alembic", raiseerr=False, x=None)
    path_to_folder = cmd_opts.config
    if not os.path.isabs(cmd_opts.config):
        cmd_opts.config = os.path.join(base_path, cmd_opts.config + "alembic.ini")
    config = Config(file_=cmd_opts.config, ini_section=cmd_opts.name, cmd_opts=cmd_opts)
    alembic_location = config.get_main_option("script_location")
    if not os.path.isabs(alembic_location):
        config.set_main_option("script_location", os.path.join(base_path, path_to_folder + alembic_location))
    config.set_main_option("sqlalchemy.url", cmd_opts.pg_url)
    return config


def update_python(migrations_count):
    old_cwd = os.getcwd()
    os.chdir(os.path.join("migrations", "python"))
    try:
        command.upgrade(make_alembic_config(), f"+{migrations_count}")
    finally:
        os.chdir(old_cwd)


def rollback_python(migrations_count):
    old_cwd = os.getcwd()
    os.chdir(os.path.join("migrations", "python"))
    try:
        command.downgrade(make_alembic_config(), f"-{migrations_count}")
    finally:
        os.chdir(old_cwd)


def update_java(migrations_count):
    p = subprocess.Popen(["liquibase", "update-count", migrations_count], cwd="migrations/java")
    p.wait()


def rollback_java(migrations_count):
    p = subprocess.Popen(["liquibase", "rollback-count", migrations_count], cwd="migrations/java")
    p.wait()
