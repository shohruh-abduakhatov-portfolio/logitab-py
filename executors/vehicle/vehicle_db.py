from asyncpg import UniqueViolationError

from executors.models.vehicle import Vehicle
from modules.core.Connector import db


async def db_add(data: Vehicle):
    vehicle = {}
    try:
        vehicle = (await db.query(
            'INSERT INTO public.vehicles (make, model, year, license_plate_no, enter_vin_manually, vin, '
            'notes, eld_id, fuel_type_id, plate_issue_state_id, vehicle_id, status, organization_id, driver_id) '
            'VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13) '
            'returning id, current_timestamp ;',
            (data.make, data.model, data.year, data.license_plate_no, data.enter_vin_manually, data.vin, data.notes,
             data.eld_id, data.fuel_type_id, data.plate_issue_state_id, data.vehicle_id, data.status,
             data.organization_id, data.driver_id)))
    except UniqueViolationError as e:
        raise e
    except Exception as e:
        pass
    return vehicle


async def db_modify(data):
    terminal = (
        await db.query(
            "UPDATE vehicles "
            "SET make = $1, model = $2, year = $3, license_plate_no = $4, enter_vin_manually = $5, vin = $6, "
            "notes = $7, eld_id = $8, fuel_type_id = $9, plate_issue_state_id = $10, vehicle_id = $11, status = $12, "
            "organization_id = $13, driver_id=$15 "
            "WHERE id = $14 returning id, current_timestamp;",
            (data.make, data.model, data.year, data.license_plate_no, data.enter_vin_manually, data.vin, data.notes,
             data.eld_id, data.fuel_type_id, data.plate_issue_state_id, data.vehicle_id, data.status,
             data.organization_id, data.id, data.driver_id)))
    return terminal


async def db_remove(id):
    terminal = await db.query('DELETE FROM vehicles where id={} returning id, current_timestamp'.format(id))
    return terminal


# async def db_get_one(id):
#     # todo join with
#     # plate_issue_state_id,
#     # fuel_type
#     result = (await db.query('select *
# from (
#          select *
#          from vehicles
#          where id = 1
#      ) as v,
#      eld as e,
#      fuel_types as ft,
#      home_terminal_timezone as ht
# where v.eld_id = e.id and v.plate_issue_state_id=', id))
#     return result


async def db_paginate(limit, offset, status, organization_id):
    query = (
        # " select v.*, e.serial_no, e.device_version, e.telematics "
        # " from (select * "
        # "       from ( "
        # "                select * "
        # "                from vehicles "
        # "                where organization_id = $4) as v_inner "
        # "       where status = $3 "
        # "       limit $1 offset $2 "
        # "      ) as v, "
        # "      eld as e "
        # " where v.eld_id = e.id; "

        "with recursive "
        "    _raw_in as ( "
        "        select * "
        "        from vehicles "
        "        where organization_id = $4 "
        "    ), "
        "    _raw as ( "
        "        select * "
        "        from _raw_in as v_inner "
        "        where status = $3 "
        "    ), "
        "    tc as ( "
        "        select count(_raw.id) "
        "        from _raw "
        "    ) "
        "select v.*, "
        "       e.serial_no, "
        "       e.device_version, "
        "       e.telematics, "
        "       (select tc.count from tc) count "
        "from (select * "
        "      from _raw "
        "      limit $1 offset $2 "
        "     ) as v, "
        "     eld as e "
        "where v.eld_id = e.id; "

    )
    result = await db.list(query,
                           (limit, offset, status, organization_id))
    data = {
        "data": result,
        "total_count": 0 if len(result) == 0 else result[0]['count']
    }
    return data


async def db_get_by_status(organization_id, status):
    query = (
        " select v.*, e.serial_no, e.device_version, e.telematics "
        " from (select * "
        "       from ( "
        "                select * "
        "                from vehicles "
        "                where organization_id = $2) as v_inner "
        "       where status = $1 "
        "      ) as v, "
        "      eld as e "
        " where v.eld_id = e.id; "
    )
    result = await db.list(query,
                           (status, organization_id))
    return result


async def db_search(limit, offset, organization_id, text):
    query = (
        "select * "
        "from ( "
        "         select v.*, e.serial_no, e.device_version, e.telematics "
        "         from ( "
        "                  select * "
        "                  from vehicles "
        "                  where organization_id = $1) as v, "
        "              eld as e "
        "         where v.eld_id = e.id "
        ") as out "
        "      where (vehicle_id||make||model||license_plate_no||serial_no||device_version||notes) "
        "                like '%{}%' "
        "      limit $2 offset $3; "
    ).format(text)

    result = await db.list(
        query,
        (organization_id, limit, offset))
    return result


async def get_all():
    result = await db.list("select * from vehicles;")
    return result
