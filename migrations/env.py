from os import environ
from logging.config import fileConfig
from alembic import context
from app.models.model_db import User, Account, Product, Transaction


config = context.config
section = config.config_ini_section
fileConfig(config.config_file_name)

config.set_section_option(section, "DB_USER", environ.get("DB_USER"))
config.set_section_option(section, "DB_PASS", environ.get("DB_PASS"))
config.set_section_option(section, "DB_NAME", environ.get("DB_NAME"))
config.set_section_option(section, "DB_HOST", environ.get("DB_HOST"))

target_metadata = [User.metadata, Account.metadata, Product.metadata, Transaction.metadata]
