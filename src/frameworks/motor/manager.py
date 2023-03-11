import logging

import certifi
import motor.motor_asyncio
from pymongo.errors import ConnectionFailure

from adapters.interfaces import DocumentDatabaseService


class MotorManager(
    DocumentDatabaseService[
        motor.motor_asyncio.AsyncIOMotorClient,
        motor.motor_asyncio.AsyncIOMotorDatabase,
    ]
):
    """Manager for Motor (Async MongoDB Client)."""

    def __init__(self, application_name: str, database_name: str, database_uri: str):
        self._logger = logging.getLogger(f"{self.__class__.__name__}")
        self._application_name = application_name
        self._database_name = database_name
        self._database_uri = database_uri
        self._client: motor.motor_asyncio.AsyncIOMotorClient | None = None

    async def connect(self) -> None:
        """Connect to a Mongodb cluster."""
        self.close()
        self._client = motor.motor_asyncio.AsyncIOMotorClient(self._database_uri, appname=self._application_name)
        try:
            await self._client.admin.command("ping")
        except ConnectionFailure:
            self._logger.info("Server [%s] not available!", self._database_uri)
        else:
            self._logger.info("Connected to MongoDB [%s].", self._database_name)

    def close(self) -> None:
        """Close the current database connection."""
        if self._client is None:
            return
        self._client.close()
        self._logger.info("Closed MongoDB connection.")

    @property
    def client(self) -> motor.motor_asyncio.AsyncIOMotorClient:
        """Return the instantiated MongoDB client."""
        if self._client is None:
            raise ValueError("There is no MongoDB client.")
        return self._client

    @property
    def database(self) -> motor.motor_asyncio.AsyncIOMotorDatabase:
        """Return the current instance of a Database client."""
        return self.client[self._database_name]
