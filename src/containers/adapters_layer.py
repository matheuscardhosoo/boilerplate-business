from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import DependenciesContainer


class AdaptersLayer(DeclarativeContainer):
    """Dependency Container for Adapters Layer."""

    # Frameworks Layer
    frameworks = DependenciesContainer()

    # Services
