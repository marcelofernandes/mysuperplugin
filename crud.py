from . import db
from loguru import logger

async def create(device_id: str) -> None:
    await db.execute(
        """
        INSERT INTO mysuperplugin.device (device_id)
        VALUES (?)
        """,
        (device_id),
    )
    return


async def update(id: str, device_id: str) -> None:
    await db.execute(
        """
            UPDATE mysuperplugin.device SET device_id = ?, time = ?
            WHERE id = ?
        """,
        (device_id, db.timestamp_now, id),
    )
    return


async def get_device(id: str):
    row = await db.fetchone(
        """SELECT * FROM mysuperplugin.device WHERE id = ?""",
        (id),
    )
    return row

async def delete_device(id: str) -> None:
    await db.execute(
        "DELETE FROM mysuperplugin.device WHERE id = ?",
        (id),
    )
