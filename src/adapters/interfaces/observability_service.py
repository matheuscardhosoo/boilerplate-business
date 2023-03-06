from abc import ABCMeta, abstractmethod
from typing import Any, Dict, Optional


class ObservabilityService(metaclass=ABCMeta):
    """A service to complement Observability reports."""

    @abstractmethod
    def set_tag(self, key: str, value: Any) -> None:
        """Set a tag to Observability reports."""

    @abstractmethod
    def set_context(self, key: str, value: Dict[str, Any]) -> None:
        """Set a context to Observability reports."""

    @abstractmethod
    def set_extra(self, key: str, value: Any) -> None:
        """Set a extra content to Observability reports."""

    @abstractmethod
    def set_user(self, value: Optional[Dict[str, Any]]) -> None:
        """Set a extra content to Observability reports."""
