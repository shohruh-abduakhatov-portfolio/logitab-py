from asyncpg import UniqueViolationError

from executors.models.event import Event
from modules.core.Connector import db


async def db_add(data: Event):
    driver_event = {}
    try:
        driver_event = (await db.query(
            'insert into events(start_datetime, duration, from_address, to_address, distance, notes, '
            'driver_id, unit_id, vehicle_id, organization_id, start_odometer, current_address, start_engine_hours, '
            'time_minute, current_lon, current_lat, event_status, log_id) '
            'values ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18) '
            'returning id, current_timestamp;',
            (data.start_datetime, data.duration, data.from_address, data.to_address, data.distance,
             data.notes, data.driver_id, data.unit_id, data.vehicle_id, data.organization_id,
             data.start_odometer, data.current_address, data.start_engine_hours, data.time_minute,
             data.current_lon, data.current_lat, data.event_status, data.log_id)))
    except UniqueViolationError as e:
        raise e
    except Exception as e:
        pass
    return driver_event


async def db_modify(data: Event):
    driver_event = (
        await db.query(
            'update events set start_datetime=$1, duration=$2, from_address=$3, to_address=$4,  '
            'distance=$5, notes=$6, driver_id=$7, unit_id=$8, vehicle_id=$9, organization_id=$10,  '
            'start_odometer=$11, time_minute=$12, start_engine_hours=$13, current_address=$14, '
            'current_lon=$16, current_lat=$17, event_status=$18, log_id=$19 '
            'where id=$15 '
            'returning *, current_timestamp;',
            (data.start_datetime, data.duration, data.from_address, data.to_address, data.distance,
             data.notes, data.driver_id, data.unit_id, data.vehicle_id, data.organization_id,
             data.start_odometer, data.time_minute, data.start_engine_hours, data.current_address, data.id,
             data.current_lon, data.current_lat, data.event_status, data.log_id)))
    return driver_event


async def db_remove(id):
    driver_event = await db.query(
        'delete from events where id = $1 returning id, driver_id, current_timestamp', (id,))
    return driver_event


async def db_bulk_get(ids, organization_id):
    result = (await db.list(
        ("select * "
         "from ( "
         "         select * "
         "         from events "
         "         where organization_id = $1) as out "
         "where id in {} "
         "order by id; "
         ).format(tuple(ids))), (organization_id,))
    return result


async def db_bulk_get_log_id(log_id):
    result = await db.list(
        "select * "
        "from events "
        "where log_id = $1 "
        "order by time_minute; "
        , (log_id,))
    return result

async def db_bulk_get_log_ids(log_ids):
    if not log_ids and isinstance(log_ids, list):
        log_ids = tuple(log_ids)
    result = await db.list((
        "select * "
        "from events "
        "where log_id in $1 "
        "order by time_minute; ").format(log_ids))
    return result


async def db_bulk_delete_by_log_id(log_id):
    result = (await db.list(
        'delete from events where log_id = $1 '
        'returning id;', (log_id,)))
    return result


async def db_copy_to_edited_event_table(log_id, organization_id):
    """
    :param log_id:
    :param organization_id:
    :return: [{'id': 7}, {'id': 8}, {'id': 9}, {'id': 10}]
    """
    result = await db.list(
        "INSERT INTO edited_events "
        "(start_datetime, duration, from_address, "
        " to_address, distance, notes, driver_id, "
        " unit_id, vehicle_id, organization_id, "
        " start_odometer, start_engine_hours, "
        " current_address, current_lon, current_lat, "
        " time_minute, event_status, log_id) "
        "    ( "
        "        SELECT start_datetime, "
        "               duration, "
        "               from_address, "
        "               to_address, "
        "               distance, "
        "               notes, "
        "               driver_id, "
        "               unit_id, "
        "               vehicle_id, "
        "               organization_id, "
        "               start_odometer, "
        "               start_engine_hours, "
        "               current_address, "
        "               current_lon, "
        "               current_lat, "
        "               time_minute, "
        "               event_status, "
        "               log_id "
        "        FROM ( "
        "                 select * "
        "                 from events "
        "                 where organization_id = $1 "
        "             ) as fin "
        "        WHERE fin.log_id = $2 "
        "    ) "
        "returning id; "
        , (organization_id, log_id))
    return result


async def db_copy_from_edited_event_table(log_id):
    """
    :param log_i
    :param organization_id:
    :return: [{'id': 7}, {'id': 8}, {'id': 9}, {'id': 10}]
    """
    result = await db.list(
        "with recursive "
        "    _insert as ( "
        "        INSERT INTO events "
        "            (start_datetime, duration, from_address, to_address, "
        "             distance, notes, driver_id, unit_id, vehicle_id, "
        "             organization_id, start_odometer, start_engine_hours, "
        "             current_address, current_lon, current_lat, time_minute, "
        "             event_status, log_id) "
        "            ( "
        "                SELECT start_datetime, "
        "                       duration, "
        "                       from_address, "
        "                       to_address, "
        "                       distance, "
        "                       notes, "
        "                       driver_id, "
        "                       unit_id, "
        "                       vehicle_id, "
        "                       organization_id, "
        "                       start_odometer, "
        "                       start_engine_hours, "
        "                       current_address, "
        "                       current_lon, "
        "                       current_lat, "
        "                       time_minute, "
        "                       event_status, "
        "                       log_id "
        "                FROM edited_events "
        "                WHERE log_id = $1) "
        "            returning * "
        "    ), "
        "    _delete as ( "
        "        delete from edited_events where log_id = $1 "
        "        returning log_id "
        "    ) "
        "select _insert.* "
        "from _insert, _delete; "
        , (log_id,))
    return result
