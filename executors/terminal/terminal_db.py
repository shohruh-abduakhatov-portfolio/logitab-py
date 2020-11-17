import json

from modules.core.Connector import db


async def db_add(data):
    terminal = (await db.query('INSERT INTO terminals (name, state_id, home_terminal_address, home_terminal_timezone_id) '
                                   'VALUES ($1, $2, $3, $4) returning id, current_timestamp;', (data['name'], data['state_id'], data['home_terminal_address'], data['home_terminal_timezone_id'])))
    return terminal


async def db_modify(data):
    terminal = (
        await db.query("UPDATE terminals SET name = $1, state_id = $2, home_terminal_address = $3, home_terminal_timezone_id = $4 "
                       "WHERE id = $5 returning id, state_id, home_terminal_address, home_terminal_timezone_id current_timestamp;", (data['name'], data['state_id'], data['home_terminal_address'], data['home_terminal_timezone_id'],
                       data['id']))
    )
    return terminal


async def db_remove(data):
    terminal = await db.query('DELETE FROM terminals where id={} returning id, current_timestamp'.format(data['id']))
    return terminal


async def db_get_one(data):
    result = (await db.query('select *, current_timestamp from terminals '
                             'where id=$1;', data["id"]))
    return result

async def get_all():
    result = await db.list("select * from terminals;")
    return result