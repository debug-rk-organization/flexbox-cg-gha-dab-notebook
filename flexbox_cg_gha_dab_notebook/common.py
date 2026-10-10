# Databricks notebook source
"""Common utilities."""

import logging
import os

from pg_composite_pipelines_configuration.configuration import Configuration
from pyspark.dbutils import DBUtils
from pyspark.sql import SparkSession





def get_logger(config=None, dbutils=None) -> logging.Logger:
    """Get a configured logger."""
    logger = logging.getLogger("flexbox_cg_gha_dab_notebook")
    # Databricks pre-configures a handler on the root logger, which causes duplicate log
    # messages for child loggers. A common but WRONG fix (e.g. the one suggested at
    # https://medium.com/@metecanakar/caveats-when-using-python-logger-in-databricks-2eaf62167c4e)
    # is to call `logging.getLogger().handlers.clear()` - this nukes ALL root logger handlers,
    # breaking logging for other libraries and the Databricks runtime itself.
    # The correct approach is to disable propagation on the child logger so its messages
    # do not bubble up to the root logger's handlers.
    if os.environ.get("DATABRICKS_RUNTIME_VERSION"):
        logger.propagate = False

    # logging.getLogger() returns a singleton - if already configured, return as-is.
    # Filter out NullHandler (commonly added by libraries as a no-op placeholder) to avoid
    # falsely treating the logger as "configured" when no real output handler exists.
    if any(filter(lambda h: not isinstance(h, logging.NullHandler), logger.handlers)):
        return logger

    if config is None:
        config = Configuration.load_for_default_environment_notebook(dbutils)

    # set to lowest level, allows handlers to filter
    logger.setLevel(logging.DEBUG)

    # stream handler for console output
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s | %(module)s | %(funcName)s | %(levelname)s: %(message)s"
    )
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # disable console noise from py4j in databricks runner
    logging.getLogger("py4j").setLevel(logging.ERROR)

    return logger
