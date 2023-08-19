import os
import motor.motor_asyncio
from dotenv import load_dotenv

load_dotenv()

class MongoDBConnect:
    """
      MongoDBConnect is a context manager which is responsible for open a mongoDB connection
      and automatic close connection after work done.
      :Parms: client_db : pass client DB
      :Return: sftp connection obj

      """

    def __init__(self):
        host = os.getenv("mongo_host")
        user = os.getenv("mongo_username")
        password = os.getenv("mongo_password")
        self.client_db = "whatsflow"
        self.server = f"mongodb+srv://{user}:{password}@{host}/"
        print(self.server)
        self.client = motor.motor_asyncio.AsyncIOMotorClient(self.server)

    async def __aenter__(self):
        return self.client[self.client_db]

    async def __aexit__(self, exc_type, exc, tb):
        if self.client:
            self.client.close