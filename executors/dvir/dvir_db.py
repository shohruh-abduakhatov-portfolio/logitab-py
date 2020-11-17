from executors.models.dvir import Dvir
from modules.core.Connector import db


async def db_add(data: Dvir):
    terminal = (await db.query(
        'INSERT INTO dvir ('
        'log_id, datetime, status_code, status_name, description, driver_signature, mechanic_signature, driver_id, '
        'vehicle_id) '
        'VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9) '
        'returning id, current_timestamp ;',
        (data.log_id, data.datetime, data.status_code, data.status_name, data.description, data.driver_signature,
         data.mechanic_signature, data.driver_id, data.vehicle_id)))
    return terminal


async def db_modify(data: Dvir):
    terminal = (
        await db.query(
            "UPDATE dvir "
            "SET "
            "log_id = $1, datetime = $2, status_code = $3, status_name = $4, description = $5, driver_signature = $6, "
            "mechanic_signature = $7, driver_id = $8, vehicle_id=$10 "
            "WHERE id = $9 "
            "returning id, current_timestamp;",
            (data.log_id, data.datetime, data.status_code, data.status_name, data.description, data.driver_signature,
             data.mechanic_signature, data.driver_id, data.id, data.vehicle_id)
        )
    )
    return terminal


async def db_remove(id):
    terminal = await db.query(
        'DELETE FROM dvir where id=$1 '
        'returning id, current_timestamp', (id,))
    return terminal


async def db_remove_by_log_id(log_id):
    terminal = await db.query(
        'DELETE FROM dvir where log_id=$1 '
        'returning id, current_timestamp', (log_id,))
    return terminal


async def db_get_by_log_id(data):
    result = (await db.list('select *, current_timestamp from dvir '
                             'where log_id=$1;', (data.log_id,)))
    return result
