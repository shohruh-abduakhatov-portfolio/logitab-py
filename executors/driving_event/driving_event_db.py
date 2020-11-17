from datetime import datetime

from modules.core.Connector import db


async def db_get_one(data):
    result = (await db.query('select *, current_timestamp from events '
                             'where id=$1;', (data["id"],)))
    return result


async def db_paginate(limit, offset, organization_id, start_date=str(datetime.now().date()),
                      end_date=str(datetime.now().date()), **kwargs):
    # and driver_id = 33 and vehicle_id = 1
    driver_query = "" if not kwargs['driver_id'] else " and driver_id = " + str(kwargs['driver_id'])
    vehicle_query = "" if not kwargs['vehicle_id'] else " and vehicle_id = " + str(kwargs['vehicle_id'])

    query = (
        "with recursive "
        "    _raw as ( "
        "        select * "
        "        from events "
        "        where organization_id = $3 "
        "          and event_status = 'd' "
        "    ), "
        "    tc as ( "
        "        select count(_raw.id) "
        "        from _raw "
        "    ) "
        " select de.*, u.first_name, u.last_name, u.phone, u.email,"
        "        (select tc.count from tc) count  "
        " from (select * "
        "       from _raw as _in "
        "    where start_datetime >= {} "
        "      and start_datetime <= {} "
        "      {} {}"
        "       limit $1 offset $2) as de, "
        "      drivers as d, "
        "      users as u "
        " where de.driver_id = d.id and d.user_id = u.id; "
    ).format(start_date, end_date, driver_query, vehicle_query)
    result = await db.list(query,
                           (limit, offset, organization_id))
    data = {
        "data": result,
        "total_count": 0 if len(result) == 0 else result[0]['count']
    }
    return data


async def db_search(limit, offset, organization_id, text):
    query = (
        " select *  "
        " from (select de.*, u.first_name, u.last_name, u.phone, u.email  "
        "       from (select *  "
        "             from events  "
        "             where organization_id = $1 and event_status = 'd' "
        "            ) as de,  "
        "            drivers as d,  "
        "            users as u  "
        "       where de.driver_id = d.id  "
        "         and d.user_id = u.id) as out  "
        " where (first_name || last_name || from_address || to_address || notes ) like '%{}%'  "
        " limit $2 offset $3;  "
    ).format(text, text)
    result = await db.list(
        query,
        (organization_id, limit, offset))
    return result


async def get_all():
    result = await db.list("select * from events;")
    return result
