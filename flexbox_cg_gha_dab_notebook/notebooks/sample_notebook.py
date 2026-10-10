# Databricks notebook source
# %sh pip install -r ../../requirements.txt
# optionally you may add these dependencies to your serverless environment as `-r ../../requirements.txt`



# COMMAND ----------
# MAGIC %run ../common

# COMMAND ----------
from pg_composite_pipelines_configuration.configuration import Configuration

config = Configuration.load_for_default_environment_notebook(dbutils)


logger = get_logger(config)

logger.info(f"hello world {config['catalog-name']}.{config['schema-name']}")
