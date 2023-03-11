from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Singleton
from fastapi import FastAPI

from adapters.views import health_check
from business.exceptions import BusinessError
from frameworks.fastapi import FastapiManager
from frameworks.motor import MotorManager


class FrameworksLayer(DeclarativeContainer):
    """Dependency Container for Frameworks Layer."""

    # Configuration
    config = Configuration()

    # Frameworks
    api_app: Singleton[FastAPI] = Singleton(
        FastAPI,
        title=config.env.provided["name"],
        description=config.env.provided["description"],
        version=config.env.provided["version"],
        debug=config.env.provided["debug"],
    )

    # Managers
    api_manager: Singleton[FastapiManager] = Singleton(FastapiManager, app=api_app)
    database_manager: Singleton[MotorManager] = Singleton(
        MotorManager,
        application_name=config.env.name,
        database_name=config.database.name,
        database_uri=config.database.uri,
    )

    @classmethod
    def initialize(cls, config: Configuration) -> "FrameworksLayer":
        """Initialize container."""
        container = cls(config=config)
        database_manager = container.database_manager()
        api_manager = container.api_manager()
        api_manager.include_router(health_check.router, "health_check")
        api_manager.add_exception_handler(BusinessError, api_manager.exception_handler)
        api_manager.add_event_handler("startup", database_manager.connect)
        api_manager.add_event_handler("shutdown", database_manager.close)
        api_manager.add_middleware(api_manager.generate_middleware_dispatch())
        container.init_resources()
        return container
