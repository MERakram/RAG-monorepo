import asyncio
from pymongo import MongoClient

from app.core.config import MONGODB_URL, MONGO_DATABASE, MONGO_COLLECTION_USERS
from app.core.security import get_password_hash
from app.model.user import UserDB

# Admin user details (customize as needed)
ADMIN_USERNAME = "admin"
ADMIN_EMAIL = "admin@example.com"
ADMIN_PASSWORD = "adminpassword"

async def seed_admin_user():
    client = MongoClient(MONGODB_URL)
    db = client[MONGO_DATABASE]
    user_collection = db[MONGO_COLLECTION_USERS]

    # Check if admin user already exists by username
    if user_collection.find_one({"username": ADMIN_USERNAME}):
        print(f"Admin user '{ADMIN_USERNAME}' already exists.")
        client.close()
        return

    hashed_password = get_password_hash(ADMIN_PASSWORD)

    admin_user_model = UserDB(
        email=ADMIN_EMAIL,
        hashed_password=hashed_password,
        active=True,
        role="admin",
        username=ADMIN_USERNAME,
    )

    admin_user_dict = admin_user_model.model_dump(by_alias=True, exclude_none=True)

    try:
        result = user_collection.insert_one(admin_user_dict)
        print(f"Admin user '{ADMIN_USERNAME}' created successfully with ID: {result.inserted_id}")
    except Exception as e:
        print(f"Error creating admin user: {e}")
    finally:
        client.close()

if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(seed_admin_user())
    finally:
        loop.close()