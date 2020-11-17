from executors.models.fuel_type import FuelType
from modules.core.Connector import db


async def db_add(data: FuelType):
    terminal = (await db.query(
        'INSERT INTO fuel_types (title, alias) '
        'VALUES ($1, $2) '
        'returning id, current_timestamp ;',
        (data.title, data.alias)))
    return terminal


async def db_modify(data):
    terminal = (
        await db.query(
            "UPDATE fuel_types "
            "SET "
            "title = $2, alias = $3 "
            "WHERE id = $1 "
            "returning id, current_timestamp;",
            (data.id, data.title, data.alias, data.id)
        )
    )
    return terminal


async def db_remove(id):
    terminal = await db.query(
        'DELETE FROM fuel_types where id={} returning id, current_timestamp'
            .format(id))
    return terminal


async def db_get_one(data):
    result = (await db.query('select *, current_timestamp from fuel_types '
                             'where id=$1;', data.id))
    return result

async def get_all():
    result = await db.list("select * from fuel_types;")
    return result