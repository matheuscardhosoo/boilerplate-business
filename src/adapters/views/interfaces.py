from abc import ABCMeta

from adapters.dtos.interfaces import DTO


class InputDTO(DTO, metaclass=ABCMeta):
    """Interface for routes input DTOs."""

    class Config:
        """Configuration class."""

        allow_mutation = False
        anystr_strip_whitespace = True
        max_anystr_length = 100


class OutputDTO(DTO, metaclass=ABCMeta):
    """Interface for routes output DTOs."""
