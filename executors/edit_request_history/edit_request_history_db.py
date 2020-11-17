from executors.models.edit_request_history import EditRequestHistory
from modules.core.Connector import db


async def db_add(data: EditRequestHistory):
    terminal = (await db.query(
        'INSERT INTO edit_request_history '
        '(log_id, created_datetime, status_name, status_desc) '
        'VALUES ($1, $2, $3, $4) '
        'returning id, current_timestamp ;',
        (data.log_id, data.created_datetime, data.status_name, data.status_desc)))
    return terminal


async def db_modify(data: EditRequestHistory):
    terminal = (
        await db.query(
            "UPDATE edit_request_history "
            "SET "
            "log_id= $1, created_datetime= $2, status_name= $3, status_desc= $4 "
            "WHERE id = $5 "
            "returning id, current_timestamp;",
            (data.log_id, data.created_datetime, data.status_name, data.status_desc, data.id))
    )
    return terminal


async def db_remove(id):
    terminal = await db.query(
        'DELETE FROM edit_request_history where id={} '
        'returning id, current_timestamp'.format(id))
    return terminal


async def db_remove_by_log_id(log_id):
    terminal = await db.query(
        'DELETE FROM edit_request_history where log_id={} '
        'returning id, current_timestamp'.format(log_id))
    return terminal


async def db_get_by_log_id(data: EditRequestHistory):
    result = (await db.list('select *, current_timestamp from edit_request_history '
                             'where log_id=$1;', (data.log_id, )))
    return result
