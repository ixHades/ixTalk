import os
import pytest
import asyncio
from tortoise import Tortoise
MODEL_MODULES = ["app.db.models.users"]


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def initialize_tests():
    await Tortoise.init(
            db_url="sqlite://:memory:",
            modules={"models": MODEL_MODULES}
    )

    await Tortoise.generate_schemas()

    yield

    await Tortoise.close_connections()
@pytest.fixture()
async def test_user():
    from app.db.models.users import Users
    import random
    user = await Users.create(user_id=random.randint(10000000,99999999))
    return user
@pytest.fixture()
async def test_admin():
    from app.db.models.admins import Admins
    from app.db.enums import AdminRole
    import random
    admin = await Admins.create(admin_user_id=random.randint(10000000,99999999), role=AdminRole.SUPER)
    return admin

