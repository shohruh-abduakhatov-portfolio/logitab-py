from executors.models.violation import Violation
from modules.core.Connector import db


async def db_add(data: Violation):
    terminal = (await db.query(
        'INSERT INTO violation ( '
        'log_id, violation, name, description, error_level_code, error_level_desc, object_name, field_name) '
        'VALUES ($1, $2, $3, $4, $5, $6, $7, $8) '
        'returning id, current_timestamp ;',
        (data.log_id, data.violation, data.name, data.description, data.error_level_code, data.error_level_desc,
         data.object_name, data.field_name)))
    return terminal


async def db_modify(data):
    terminal = (
        await db.query(
            "UPDATE violation "
            "SET "
            "log_id=$1, violation=$2, name=$3, description=$4, error_level_code=$5, error_level_desc=$6, "
            "object_name=$7, field_name=$8 "
            "WHERE id = $9 "
            "returning id, current_timestamp;",
            (data.log_id, data.violation, data.name, data.description, data.error_level_code,
             data.error_level_desc, data.object_name, data.field_name, data.id)
        )
    )
    return terminal


async def db_remove(id):
    terminal = await db.query(
        'DELETE FROM violation where id=$1 '
        'returning id, current_timestamp', (id,))
    return terminal


async def db_remove_by_log_id(log_id):
    terminal = await db.query(
        'DELETE FROM violation where log_id=$1 '
        'returning id, current_timestamp', (log_id,))
    return terminal


async def db_get_by_log_id(data: Violation):
    result = (await db.list(
        'select *, current_timestamp from violation '
        'where log_id=$1;', (data.log_id,)))
    return result
