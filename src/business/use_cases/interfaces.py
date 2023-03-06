from abc import ABCMeta, abstractmethod

from business.ports.interfaces import Port


class InputPort(Port, metaclass=ABCMeta):
    """Interface for Use Cases input parameters."""


class OutputPort(Port, metaclass=ABCMeta):
    """Interface for Use Cases output parameters."""


class UseCase(metaclass=ABCMeta):
    """Interface for UseCase classes."""

    @abstractmethod
    async def execute(self, input_port: InputPort) -> OutputPort:
        """Execute an use case."""
