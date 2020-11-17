from executors.models.eld import Eld
from executors.models.organization import Organization
from modules.core.Connector import db


async def db_add(data: Organization):
    terminal = (await db.query(
        'INSERT INTO organisations (title) '
        'VALUES ($1) '
        'returning id, current_timestamp ;',
        (data.title,)))
    return terminal


async def db_modify(data: Organization):
    terminal = (
        await db.query(
            "UPDATE organisations "
            "SET "
            "title = $1 "
            "WHERE id = $2 "
            "returning id, current_timestamp;",
            (data.title, data.id)
        )
    )
    return terminal


async def db_remove(id):
    terminal = await db.query('DELETE FROM organisations where id={} returning id, current_timestamp'.format(id))
    return terminal


async def db_get_one(data: Organization):
    result = (await db.query('select *, current_timestamp from organisations '
                             'where id=$1;', data.id))
    return result


async def get_all():
    result = await db.list("select * from organisations;")
    return result