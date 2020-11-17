import json

from executors.models.unit import Units
from modules.core.Connector import db


async def db_add(data: Units):
    terminal = (await db.query(
        'INSERT INTO public.units '
        '(notes, icon, driver_id, vehicle_id, groups) '
        'VALUES ($1, $2, $3, $4, $5) '
        'returning id, current_timestamp ;',
        (data.notes,
         data.icon,
         data.driver_id,
         data.vehicle_id,
         json.dumps(data.groups))))
    return terminal


async def db_modify(data: Units):
    terminal = (
        await db.query(
            "UPDATE public.units "
            "SET "
            "notes = $1, icon = $2, driver_id = $3, vehicle_id = $4, groups = $5 "
            "WHERE id = $6 "
            "returning id, current_timestamp;",
            (data.notes, data.icon, data.driver_id, data.vehicle_id, json.dumps(data.groups), data.id))
    )
    return terminal


async def db_remove(id):
    terminal = await db.query('DELETE FROM units where id={} returning id, current_timestamp'.format(id))
    return terminal


async def db_get_one(data):
    result = (await db.query('select *, current_timestamp from units '
                             'where id=$1;', data["id"]))
    result['groups'] = json.loads(result['groups'])
    return result


async def db_paginate(limit, offset, organization_id):
    query = (
        "with recursive "
        "    _raw as ( "
        "        select * "
        "        from units "
        "        where organization_id = $3 "
        "    ), "
        "    tc as ( "
        "        select count(_raw.id) "
        "        from _raw "
        "    ) "
        "select un.*, "
        "       v.make, "
        "       v.model, "
        "       v.year, "
        "       v.license_plate_no, "
        "       v.vin, "
        "       v.status                  vehicle_status, "
        "       v.notes                   vehicle_note, "
        "       d.driver_license_no, "
        "       d.co_driver_id, "
        "       d.trailer_no, "
        "       d.note                    driver_note, "
        "       d.activated_datetime, "
        "       d.terminated_datetime, "
        "       d.terminal_id, "
        "       d.status                  driver_status, "
        "       d.driver_code, "
        "       (select tc.count from tc) count "
        "from ( "
        "         select * "
        "         from _raw "
        "         limit $1 offset $2 "
        "     ) as un, "
        "     drivers as d, "
        "     vehicles as v, "
        "     users as u "
        "where un.driver_id = d.id "
        "  and d.user_id = u.id "
        "  and un.vehicle_id = v.id; "
    )
    result = await db.list(query, (limit, offset, organization_id))
    try:
        for row in result:
            row['groups'] = json.loads(row['groups'])
    except:
        pass
    data = {
        "data": result,
        "total_count": 0 if len(result) == 0 else result[0]['count']
    }
    return data


async def db_search(limit, offset, organization_id, text):
    query = (
        "select * "
        "from (select un.*, "
        "             v.make, "
        "             v.model, "
        "             v.year, "
        "             v.license_plate_no, "
        "             v.vin, "
        "             v.status as vehicle_status, "
        "             v.notes  as vehicle_note, "
        "             d.driver_license_no, "
        "             d.co_driver_id, "
        "             d.trailer_no, "
        "             d.note   as driver_note, "
        "             d.activated_datetime, "
        "             d.terminated_datetime, "
        "             d.terminal_id, "
        "             d.status as driver_status, "
        "             d.driver_code, "
        "             u.first_name, "
        "             u.last_name, "
        "             u.phone, "
        "             u.email, "
        "             u.username "
        "      from ( "
        "               select * "
        "               from units "
        "               where organization_id = $1 "
        "           ) as un, "
        "           drivers as d, "
        "           vehicles as v, "
        "           users as u "
        "      where un.driver_id = d.id "
        "        and d.user_id = u.id "
        "        and un.vehicle_id = v.id) as _out "
        "where (notes || first_name || last_name || phone || trailer_no || driver_code) like '%driver_code%' "
        "limit $2 offset $3; "
    ).format(text)

    result = await db.list(query, (organization_id, limit, offset))
    try:
        for row in result:
            row['groups'] = json.loads(row['groups'])
    except:
        pass
    return result


async def get_all():
    result = await db.list("select * from units;")
    try:
        for row in result:
            row['groups'] = json.loads(row['groups'])
    except:
        pass
    return result
