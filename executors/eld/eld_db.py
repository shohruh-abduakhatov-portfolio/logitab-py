from executors.models.eld import Eld
from modules.core.Connector import db


async def db_add(data: Eld):
    terminal = (await db.query(
        'INSERT INTO eld (serial_no, device_version, telematics, notes, organization_id) '
        'VALUES ($1, $2, $3, $4, $5) '
        'returning id, current_timestamp ;',
        (data.serial_no, data.device_version, data.telematics, data.notes, data.organization_id)))
    return terminal


async def db_modify(data):
    terminal = (
        await db.query(
            "UPDATE eld "
            "SET "
            "serial_no = $1, device_version = $2, telematics = $3, notes = $4, organization_id=$5 "
            "WHERE id = $6 "
            "returning id, current_timestamp;",
            (data.serial_no, data.device_version, data.telematics, data.notes, data.organization_id, data.id)
        )
    )
    return terminal


async def db_remove(id):
    terminal = await db.query('DELETE FROM eld where id={} returning id, current_timestamp'.format(id))
    return terminal


async def db_get_one(data):
    result = (await db.query('select *, current_timestamp from eld '
                             'where id=$1;', data.id))
    return result


async def db_paginate(limit, offset, organization_id):
    result = await db.list(
        "with recursive "
        "    _raw as ( "
        "        select * "
        "        from eld "
        "        where organization_id = $3 "
        "    ), "
        "    tc as ( "
        "        select count(_raw.id) "
        "        from _raw "
        "    ) "
        "select p.*, (select tc.count from tc) count from "
        "   _raw as p "
        "limit $1 offset $2;",
        (limit, offset, organization_id))
    data = {
        "data": result,
        "total_count": 0 if len(result) == 0 else result[0]['count']
    }
    return data


async def db_get_by_org_id(organization_id):
    result = await db.list(
        "select * from eld where organization_id = $1;",
        (organization_id,))
    return result


async def db_search(limit, offset, organization_id, text):
    result = await db.list(
        ("select * from "
         "   (select * from eld where organization_id = $1) as p "
         "where (serial_no||notes) like '%{}%' "
         "limit $2 offset $3;").format(text),
        (organization_id, limit, offset))
    return result


async def get_all():
    result = await db.list("select * from eld;")
    return result
