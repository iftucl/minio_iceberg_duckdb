from fastapi.exceptions import HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
import asyncio
import os

from modules.api_models import CreateUserRequest, MongoTraderUser

__doc__ = """
==================================================
Functionality to read write User Auth to Mongodb.
==================================================

"""

async def get_user(user: str) -> dict:
    """
    Get the trader user info stored in mongodb.

    :param user: trader unique id

    Examples:
    ---------
        >>> import asyncio
        >>> loop = asyncio.get_event_loop()
        >>> loop.run_until_complete(get_user(user="foo"))
    """
    client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
    db = client.Users

    document = await db['TradeUsers'].find_one({'username': user})
    
    if not document:        
        return False
    return MongoTraderUser(**document)

async def create_user(new_user: CreateUserRequest) -> dict:
    """
    Create a user in MongoDB.

    Examples:
    ---------
        >>> import asyncio
        >>> new_user_model = CreateUserRequest(username="foo", password="bar", email="foo@bar.com")
        >>> loop = asyncio.get_event_loop()
        >>> loop.run_until_complete(create_user(new_user=new_user_model))
        InsertOneResult(ObjectId('67839509d474445b2bbebf46'), acknowledged=True)
    """
    check_user = await get_user(user = new_user.username)
    if check_user:
        raise HTTPException(status_code=409, detail="Resource already exists")

    client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
    db = client.Users
    load_data = await db["TradeUsers"].insert_one(new_user.model_dump())
    return load_data
