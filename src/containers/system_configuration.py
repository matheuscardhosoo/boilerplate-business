import logging.config
import os

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration

from __init__ import __version__


class SystemConfiguration(DeclarativeContainer):
    """Dependency Container for configuration resources"""

    config = Configuration()

    @classmethod
    def initialize(cls) -> "SystemConfiguration":
        """Initialize container."""
        path: str = os.environ.get("CONFIG_PATH", "containers/system_configuration.yaml")
        container = cls()
        container.config.from_yaml(path)
        container.config.env.service_name.from_env("SERVICE_NAME", "boilerplate-domain-mongodb")
        container.config.env.env.from_env("ENV", "test")
        container.config.env.debug.from_env("DEBUG", True)
        container.config.env.version.from_env("VERSION", __version__)
        container.config.logging.handlers.console.level.from_env("LOG_LEVEL", "INFO")
        container.config.logging.root.level.from_env("LOG_LEVEL", "INFO")
        container.config.database.name.from_env("DB_NAME", "boilerplate-business")
        container.config.database.uri.from_env("DB_URI", "mongodb://localhost:27017")
        container.init_resources()
        logging_config = container.config.logging()
        logging.config.dictConfig(config=logging_config)
        return container
