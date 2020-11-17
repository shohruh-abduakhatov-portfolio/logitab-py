from asyncpg import UniqueViolationError

from executors.models.driver import Driver
from modules.core.Connector import db


async def db_add(data: Driver):
    result = {}
    try:
        result = (await db.query(
            "INSERT INTO drivers "
            "(driver_license_no, co_driver_id, trailer_no, note, enable_for_elds, enable_for_elog, allow_yard_move, "
            "allow_personal_conveyance, activated_datetime, terminated_datetime, app_version, status, color, "
            "device_version_id, driver_license_issue_state_id, terminal_id, vehicle_id, user_id, organization_id, "
            "driver_code, date_created) "
            "VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20, $21) "
            "RETURNING id, current_timestamp;",
            (data.driver_license_no, data.co_driver_id, data.trailer_no, data.note, data.enable_for_elds,
             data.enable_for_elog, data.allow_yard_move, data.allow_personal_conveyance, data.activated_datetime,
             data.terminated_datetime, data.app_version, data.status, data.color, data.device_version_id,
             data.driver_license_issue_state_id, data.terminal_id, data.vehicle_id, data.user_id,
             data.organization_id, data.driver_code, data.date_created)))
    except UniqueViolationError as e:
        raise e
    except Exception as e:
        pass
    return result


async def db_modify(data: Driver):
    driver = (
        await db.query(
            "UPDATE drivers "
            "SET driver_license_no=$1, co_driver_id=$2, trailer_no=$3, note=$4, enable_for_elds=$5, "
            "enable_for_elog=$6, allow_yard_move=$7, allow_personal_conveyance=$8, activated_datetime=$9, "
            "terminated_datetime=$10, app_version=$11, status=$12, color=$13, device_version_id=$14, "
            "driver_license_issue_state_id=$15, terminal_id=$16, vehicle_id=$17, user_id=$18, "
            "organization_id=$19, driver_code=$21, date_created=$22 "
            "WHERE id = $20 "
            "returning *, current_timestamp;",
            (data.driver_license_no, data.co_driver_id, data.trailer_no, data.note, data.enable_for_elds,
             data.enable_for_elog, data.allow_yard_move, data.allow_personal_conveyance, data.activated_datetime,
             data.terminated_datetime, data.app_version, data.status, data.color, data.device_version_id,
             data.driver_license_issue_state_id, data.terminal_id, data.vehicle_id, data.user_id,
             data.organization_id, data.id, data.driver_code, data.date_created))
    )
    return driver


async def db_remove(data):
    driver = await db.query('DELETE FROM drivers where id=$1 '
                            'returning current_timestamp', (data.id,))
    return driver


async def db_get_by_id(data):
    result = (await db.query('select *, current_timestamp from drivers '
                             'where id=$1;', (data.id,)))
    return result


# async def db_get_by_status(data):
#     result = (await db.query('select *, current_timestamp from drivers '
#                              'where status=$1;', (data.status,)))
#     return result


async def db_paginate(limit, offset, status, organization_id):
    query = (
        # "select d.*, "
        # "       e.serial_no, e.device_version, e.telematics, "
        # "       v.vehicle_id,v.model, v.make, "
        # "       u.first_name, u.last_name "
        # "from (select * "
        # "      from (select * from drivers where organization_id = $4) as v_inner "
        # "      where status = $3 "
        # "      limit $1 offset $2) as d, "
        # "     users as u, "
        # "     eld as e, "
        # "     vehicles as v "
        # "where d.device_version_id = e.id "
        # "   and d.vehicle_id = v.id "
        # "   and d.user_id = u.id; "

        "with recursive "
        "    _raw_in as ( "
        "        select * "
        "        from drivers "
        "        where organization_id = $4 "
        "    ), "
        "    _raw as ( "
        "        select * "
        "        from _raw_in "
        "        where status = $3 "
        "    ), "
        "    tc as ( "
        "        select count(_raw.id) "
        "        from _raw "
        "    ) "
        "select d.*, "
        "       e.serial_no, "
        "       e.device_version, "
        "       e.telematics, "
        "       v.vehicle_id, "
        "       v.model, "
        "       v.make, "
        "       u.first_name, "
        "       u.last_name, "
        "       (select tc.count from tc) count "
        "from (select * "
        "      from _raw "
        "      limit $1 offset $2) as d, "
        "     users as u, "
        "     eld as e, "
        "     vehicles as v "
        "where d.device_version_id = e.id "
        "  and d.vehicle_id = v.id "
        "  and d.user_id = u.id; "

    )
    result = await db.list(
        query, (limit, offset, status, organization_id))

    data = {
        "data": result,
        "total_count": 0 if len(result) == 0 else result[0]['count']
    }
    return data


async def db_get_by_status(organization_id, status):
    query = (
        "select d.*, "
        "       v.vehicle_id vehicle_code, v.make, v.model, v.year, "
        "       v.license_plate_no, v.enter_vin_manually, v.vin, v.status vehicle_status, "
        "       e.serial_no, e.device_version, e.telematics, "
        "       u.first_name, u.last_name "
        "from (select * "
        "      from ( "
        "               select * "
        "               from drivers "
        "               where organization_id = $2) as v_inner "
        "      where status = $1 "
        "     ) as d, "
        "      users as u, "
        "      eld as e, "
        "      vehicles as v "
        "where d.device_version_id = e.id "
        "  and d.vehicle_id = v.id "
        "  and d.user_id = u.id; "
    )
    result = await db.list(query, (status, organization_id))
    return result


async def db_search(limit, offset, organization_id, text):
    query = (
        "select * "
        "from ( "
        "         select d.*, "
        "                e.serial_no, "
        "                e.device_version, "
        "                e.telematics, "
        "                v.vehicle_id vehicle_code, "
        "                v.model, "
        "                v.make, "
        "                v.year, "
        "                u.first_name, "
        "                u.last_name "
        "         from ( "
        "                  select * "
        "                  from drivers "
        "                  where organization_id = $1 "
        "              ) as d, "
        "              users as u, "
        "              eld as e, "
        "              vehicles as v "
        "         where d.device_version_id = e.id "
        "           and d.vehicle_id = v.id "
        "           and d.user_id = u.id "
        "     ) as out "
        "where (first_name || last_name || device_version || co_driver_id || vehicle_code || note) "
        "          like '%{}%'  or driver_code  like '%{}%' "
        "limit $2 offset $3; "
    ).format(text, text)

    result = await db.list(
        query,
        (organization_id, limit, offset))
    return result


async def get_all():
    result = await db.list("select * from drivers;")
    return result


async def db_get_by_user_id(user_id):
    result = await db.query("select *, current_timestamp from drivers where user_id = $1 ", (user_id,))
    return result
