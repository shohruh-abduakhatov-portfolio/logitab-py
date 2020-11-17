import json

from executors.models.groups import Groups
from modules.core.Connector import db


async def db_add(data: Groups):
    terminal = (await db.query(
        'INSERT INTO groups (name, note, units_count, units, organization_id) '
        'VALUES ($1, $2, $3, $4, $5) '
        'returning id, current_timestamp ;',
        (data.name, data.note, data.units_count, json.dumps(data.units), data.organization_id)))
    return terminal


async def db_modify(data):
    terminal = (
        await db.query(
            "UPDATE groups "
            "SET "
            "name =  $1, note = $2, units_count = $3, units = $4, organization_id=$5 "
            "WHERE id = $6 "
            "returning id, current_timestamp;",
            (data.name, data.note, data.units_count, json.dumps(data.units), data.organization_id, data.id)
        )
    )
    return terminal


async def db_remove(id):
    terminal = await db.query('DELETE FROM groups where id={} returning id, current_timestamp'.format(id))
    return terminal


async def db_get_one(data):
    result = (await db.query('select *, current_timestamp from groups '
                             'where id=$1;', data.id))
    result['units'] = json.loads(result['units'])
    return result


async def db_paginate(limit, offset, organization_id):
    result = await db.list(
        "with recursive "
        "    _raw as ( "
        "        select * "
        "        from groups "
        "        where organization_id = $3 "
        "    ), "
        "    tc as ( "
        "        select count(_raw.id) "
        "        from _raw "
        "    ) "
        "select *, (select tc.count from tc) count from _raw "
        "limit $1 offset $2;",
        (limit, offset, organization_id))
    try:
        for row in result:
            row['units'] = json.loads(row['units'])
    except:
        pass
    data = {
        "data": result,
        "total_count": 0 if len(result) == 0 else result[0]['count']
    }
    return data


async def db_get_by_org_id(organization_id):
    result = await db.list(
        "select * from groups where organization_id = $1;",
        (organization_id,))
    try:
        for row in result:
            row['units'] = json.loads(row['units'])
    except:
        pass
    return result


async def db_search(limit, offset, organization_id, text):
    result = await db.list(
        ("select * from "
         "   (select * from groups where organization_id = $1) as p "
         "where (name||note) like '%{}%' "
         "limit $2 offset $3;").format(text),
        (organization_id, limit, offset))
    try:
        for row in result:
            row['units'] = json.loads(row['units'])
    except:
        pass
    return result


async def get_all():
    result = await db.list("select * from groups ;")
    try:
        for row in result:
            row['units'] = json.loads(row['units'])
    except:
        pass
    return result
