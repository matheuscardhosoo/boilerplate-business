from abc import ABCMeta

from pydantic import BaseModel


class Port(BaseModel, metaclass=ABCMeta):
    """Base class for Port objects."""

    class Config:
        """Configuration class."""

        allow_mutation = False
        extra = "ignore"
