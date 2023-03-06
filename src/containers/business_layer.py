from dependency_injector.containers import DeclarativeContainer, WiringConfiguration
from dependency_injector.providers import DependenciesContainer, Factory

from business.use_cases import CheckHealthUseCase


class BusinessLayer(DeclarativeContainer):
    """Dependency Container for Business Layer."""

    wiring_config = WiringConfiguration(packages=["adapters.views"])

    # Adapters Layer
    adapters = DependenciesContainer()

    # Use Cases
    check_health: Factory[CheckHealthUseCase] = Factory(CheckHealthUseCase)
