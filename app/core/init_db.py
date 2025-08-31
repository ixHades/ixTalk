from tortoise import Tortoise, run_async
from app.core.config import DB_URL


async def init_db():

    await Tortoise.init(db_url=DB_URL, modules={"models": ["app.db.models"]})
    await Tortoise.generate_schemas()


run_async(init_db())
