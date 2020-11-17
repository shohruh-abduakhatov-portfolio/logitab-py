from modules.core.Connector import db


async def db_add(data):
    terminal = (await db.query('INSERT INTO home_terminal_timezone (title, alias) '
                               'VALUES ($1, $2) returning id, current_timestamp;',
                               (data['title'], data['alias'])))
    return terminal


async def db_modify(data):
    terminal = (
        await db.query(
            "UPDATE home_terminal_timezone SET title = $1, alias = $2 "
            "WHERE id = $3 returning id, current_timestamp;",
            (data['title'], data['alias'], data['id']))
    )
    return terminal


async def db_remove(data):
    terminal = await db.query('DELETE FROM home_terminal_timezone where id={} returning id, current_timestamp'
                              .format(data['id']))
    return terminal


async def db_get_one(data):
    result = (await db.query('select *, current_timestamp from home_terminal_timezone '
                             'where id=$1;', data["id"]))
    return result


async def get_all():
    result = await db.list("select * from home_terminal_timezone;")
    return result
