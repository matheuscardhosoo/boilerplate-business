import logging

import certifi
from motor.core import AgnosticDatabase
from motor.motor_asyncio import AsyncIOMotorClient

from adapters.interfaces import DocumentDatabaseService


class MotorManager(DocumentDatabaseService):
    """Manager for Motor (Async MongoDB Client)."""

    def __init__(self, application_name: str, database_name: str, db_uri: str):
        self._logger = logging.getLogger(f"{self.__class__.__name__}")
        self._application_name = application_name
        self._database_name = database_name
        self._db_uri = db_uri
        self._client: AsyncIOMotorClient | None = None

    def connect(self) -> None:
        """Connect to a Mongodb cluster."""
        self.close()
        self._client = AsyncIOMotorClient(self._db_uri, appname=self._application_name, tlsCAFile=certifi.where())
        self._client.admin.command("ismaster")
        self._logger.info("Connected to MongoDB [%s].", self._database_name)

    def close(self) -> None:
        """Close the current database connection."""
        if self._client is None:
            return
        self._client.close()
        self._logger.info("Closed MongoDB connection.")

    @property
    def client(self) -> AsyncIOMotorClient:
        """Return the instantiated MongoDB client."""
        if self._client is None:
            raise ValueError("There is no MongoDB client.")
        return self._client

    @property
    def database(self) -> AgnosticDatabase:
        """Return the current instance of a Database client."""
        return self.client[self._database_name]
