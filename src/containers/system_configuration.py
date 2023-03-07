import logging.config
import os

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Resource

from __init__ import __version__


class SystemConfiguration(DeclarativeContainer):
    """Dependency Container for configuration resources"""

    config_path: str = os.environ.get("CONFIG_PATH", "src/containers/system_configuration.yaml")
    config = Configuration(yaml_files=[config_path])
    logging = Resource(logging.config.dictConfig, config=config.logging)

    @classmethod
    def initialize(cls) -> "SystemConfiguration":
        """Initialize container."""
        container = cls()
        container.config.env.env.from_env("ENV", "test")
        container.config.env.debug.from_env("DEBUG", True)
        container.config.env.version.from_env("VERSION", __version__)
        container.config.logging.handlers.console.level.from_env("LOG_LEVEL", "INFO")
        container.config.logging.root.level.from_env("LOG_LEVEL", "INFO")
        container.config.database.name.from_env("DB_NAME", "boilerplate-business-test")
        container.config.database.uri.from_env("DB_URI", "mongodb://localhost:27017")
        container.config.observability.sentry.dsn.from_env("SENTRY_DSN", None)
        container.config.observability.sentry.release.from_env("SENTRY_RELEASE", None)
        container.init_resources()
        return container
