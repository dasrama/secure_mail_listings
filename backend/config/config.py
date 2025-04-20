import asyncio
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from backend.config.settings import Settings
from backend.models.email import Email
from backend.models.user import User


class MongoClient:
    def __init__(self, uri: str, db_name: str):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[db_name]

    async def initialize(self):
        await init_beanie(
            database=self.db,
            document_models=[
                Email,
                User
            ]
        )

    @asynccontextmanager
    async def start_transaction(self) -> AsyncIterator[Any]:
        async with await self.client.start_session() as session:
            async with session.start_transaction():
                yield session

mongo_client = MongoClient(Settings().DATABASE_URL, "Secure-mail-listings")

async def initiate_database():
    await mongo_client.initialize()
