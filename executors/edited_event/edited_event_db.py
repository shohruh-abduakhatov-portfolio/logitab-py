from asyncpg import UniqueViolationError

from executors.models.edited_event import EditedEvent
from modules.core.Connector import db


async def db_add(data: EditedEvent):
    driver_event = {}
    try:
        driver_event = (await db.query(
            'insert into edited_events(start_datetime, duration, from_address, to_address, distance, notes, '
            'driver_id, unit_id, vehicle_id, organization_id, start_odometer, current_address, start_engine_hours, '
            'time_minute, current_lon, current_lat, event_status, log_id, edited_datetime, edited_status_code, '
            'edited_status_desc) '
            'values ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18) '
            'returning id, current_timestamp;',
            (data.start_datetime, data.duration, data.from_address, data.to_address, data.distance,
             data.notes, data.driver_id, data.unit_id, data.vehicle_id, data.organization_id,
             data.start_odometer, data.current_address, data.start_engine_hours, data.time_minute,
             data.current_lon, data.current_lat, data.event_status, data.log_id, data.edited_datetime,
             data.edited_status_code, data.edited_status_desc)))
    except UniqueViolationError as e:
        raise e
    except Exception as e:
        pass
    return driver_event


async def db_modify(data: EditedEvent):
    driver_event = (
        await db.query(
            'update edited_events set start_datetime=$1, duration=$2, from_address=$3, to_address=$4,  '
            'distance=$5, notes=$6, driver_id=$7, unit_id=$8, vehicle_id=$9, organization_id=$10,  '
            'start_odometer=$11, time_minute=$12, start_engine_hours=$13, current_address=$14, '
            'current_lon=$16, current_lat=$17, event_status=$18, log_id=$19, edited_datetime=$20, '
            'edited_status_code=$21, edited_status_desc=$22 '
            'where id=$15 '
            'returning *, current_timestamp;',
            (data.start_datetime, data.duration, data.from_address, data.to_address, data.distance,
             data.notes, data.driver_id, data.unit_id, data.vehicle_id, data.organization_id,
             data.start_odometer, data.time_minute, data.start_engine_hours, data.current_address, data.id,
             data.current_lon, data.current_lat, data.event_status, data.log_id, data.edited_datetime,
             data.edited_status_code, data.edited_status_desc)))
    return driver_event


async def db_remove(id):
    driver_event = await db.query(
        'delete from edited_events where id = {} returning id, driver_id, current_timestamp'.format(id))
    return driver_event


async def db_bulk_get(ids, organization_id):
    result = await db.query(
        "select * "
        "from ( "
        "         select * "
        "         from edited_events "
        "         where organization_id = $1) as out "
        "where id  {} "
        "order by id; ", (organization_id,))
    return result


async def db_bulk_get_by_log_id(log_id):
    result = await db.list(
        "select * from edited_events "
        "where log_id = $1 "
        "order by time_minute; ",
        (log_id,))
    return result


async def db_bulk_delete_by_log_id(log_id):
    result = await db.list(
        "delete from events "
        "where log_id = $1 "
        "returning id",
        (log_id,))
    return result


async def db_bulk_delete(ids):
    result = (await db.query(
        'delete from events where id in {};'
            .format(tuple(ids))))
    return result


async def db_bulk_insert(data):
    fmt = (
        "({start_datetime}, {duration}, '{from_address}', '{to_address}', {distance}, '{notes}', "
        "{driver_id}, {unit_id}, {vehicle_id}, {organization_id}, start_odometer, '{current_address}', "
        "{start_engine_hours}, {time_minute}, {current_lon}, {current_lat}, {event_status}, {log_id}, "
        "{edited_datetime}, {edited_status_code}, {edited_status_desc})"
    )
    vals = []
    for i in data:
        vals.append(fmt.format(**i))
    query = (
        'insert into edited_events(start_datetime, duration, from_address, to_address, distance, notes, '
        'driver_id, unit_id, vehicle_id, organization_id, start_odometer, current_address, start_engine_hours, '
        'time_minute, current_lon, current_lat, event_status, log_id, edited_datetime, edited_status_code, '
        'edited_status_desc) '
        'values {} '
        'returning *, current_timestamp;'
    ).format(", ".join(vals))

    driver_event = {}
    try:
        driver_event = (await db.list(query))
    except UniqueViolationError as e:
        raise e
    except Exception as e:
        pass
    return driver_event


async def db_get_by_status(status_code, org_id, driver_id):
    result = await db.list(
        "select * "
        "from ( "
        "         select * "
        "         from edited_events "
        "         where organization_id = $1 "
        "     ) as _raw "
        "where driver_id = $2 "
        "and edited_status_code = $3 "
        "order by log_id, time_minute ",
        (org_id, driver_id, status_code))
    return result


async def db_get_first_by_status(status_code, org_id, driver_id):
    result = await db.list(
        "select distinct on (log_id) * "
        "from ( "
        "         select * "
        "         from edited_events "
        "         where organization_id = $1 "
        "     ) as _raw "
        "where driver_id = $2 "
        "and edited_status_code = $3 "
        "order by log_id ",
        (org_id, driver_id, status_code))
    return result
