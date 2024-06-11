from . import db
from loguru import logger

async def create(payment_id: str) -> None:
    logger.info(payment_id)
    await db.execute(
        """
        INSERT INTO mysuperplugin.payment (payment_id)
        VALUES (?)
        """,
        (payment_id),
    )
    return


async def update(id: str, device_id: str) -> None:
    await db.execute(
        """
            UPDATE mysuperplugin.payment SET device_id = ?, time = ?
            WHERE id = ?
        """,
        (device_id, db.timestamp_now, id),
    )
    return


async def get_device(id: str):
    row = await db.fetchone(
        """SELECT * FROM mysuperplugin.payment WHERE id = ?""",
        (id),
    )
    return row

async def delete_device(id: str) -> None:
    await db.execute(
        "DELETE FROM mysuperplugin.payment WHERE id = ?",
        (id),
    )
