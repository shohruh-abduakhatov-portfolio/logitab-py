import json
from datetime import datetime

from executors.models.log import Log
from executors.utils.enum import ViolationName
from modules.core.Connector import db


async def db_add(data: Log):
    terminal = (await db.query(
        'INSERT INTO log (date, edited_event_ids, driver_id, vehicle_id, terminal_id, organization_id, '
        'break, driving, shift, cycle, signature_url, event_ids, notes, shipping_docs) '
        'VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13) '
        'returning id, current_timestamp ;',
        (data.date, json.dumps(data.edited_event_ids), data.driver_id, data.vehicle_id, data.terminal_id,
         data.organization_id, data.break_time, data.driving, data.shift, data.cycle, data.signature_url,
         data.event_ids, data.notes, data.shipping_docs, data.current_edit_request_report_url,
         data.edited_edit_request_report_url)))
    return terminal


async def db_modify(data: Log):
    terminal = await db.query(
        "UPDATE log "
        "SET "
        "date = $1, edited_event_ids = $2, driver_id = $3, vehicle_id = $4, terminal_id = $5, organization_id = $6, "
        "break = $7, driving = $8, shift = $9, cycle = $10, signature_url = $11, event_ids=$13, notes=$14, "
        "shipping_docs=$15, current_edit_request_report_url=$16, edited_edit_request_report_url=$17 "
        "WHERE id = $12 "
        "returning id, current_timestamp;",
        (data.date, json.dumps(data.edited_event_ids), data.driver_id, data.vehicle_id, data.terminal_id,
         data.organization_id, data.break_time, data.driving, data.shift, data.cycle, data.signature_url, data.id,
         data.event_ids, data.notes, data.shipping_docs, data.current_edit_request_report_url,
         data.edited_edit_request_report_url)
    )
    return terminal


async def db_remove(id):
    terminal = await db.query('DELETE FROM log where id={} returning id, current_timestamp'.format(id))
    return terminal


async def db_get_one(data):
    result = (await db.query('select *, current_timestamp from log '
                             'where id=$1;', data.id))
    if not result:
        result['event_ids'] = json.dumps(result['event_ids'])
        result['edited_event_ids'] = json.dumps(result['edited_event_ids'])
        result['shipping_docs'] = json.dumps(result['shipping_docs'])
    return result


async def db_exist_date(date=str(datetime.now().date())):
    result = (await db.query('select *, current_timestamp from log '
                             'where date=$1;', date))
    if not result:
        result['event_ids'] = json.dumps(result['event_ids'])
        result['edited_event_ids'] = json.dumps(result['edited_event_ids'])
        result['shipping_docs'] = json.dumps(result['shipping_docs'])
    return result


async def db_paginate(limit, offset, organization_id,
                      start_date=str(datetime.now().date()),
                      end_date=str(datetime.now().date()),
                      **kwargs):
    args = [limit, offset, organization_id]

    start_date = str(start_date) if isinstance(start_date, (datetime, datetime.date)) else start_date
    end_date = str(end_date) if isinstance(end_date, (datetime, datetime.date)) else end_date

    vehicle_filter = kwargs.get("vehicle", "")
    driver_filter = kwargs.get("driver", "")
    violation_filter = kwargs.get("violation", "")
    dvir_filter = kwargs.get("dvir", "")
    order_by = kwargs.get("order_by", "")

    if violation_filter:
        args.append(violation_filter)
        violation_filter = "and vi.error_level_code = $%d " % (len(args) + 1)
    if dvir_filter:
        args.append(dvir_filter)
        dvir_filter = " and dv.status_code = $%d " % (len(args) + 1)
    if vehicle_filter:
        args.append(vehicle_filter)
        vehicle_filter = " and r.vehicle_id = $%d " % (len(args) + 1)
    if driver_filter:
        args.append(driver_filter)
        driver_filter = " and r.driver_id = $%d " % (len(args) + 1)
    if order_by:
        args.append(order_by)
        order_by = " $%d " % (len(args) + 1)
    else:
        order_by = " date "

    query = (
        "with recursive "
        "    _raw as ( "
        "        select * "
        "        from ( "
        "                 select * "
        "                 from log "
        "                 where organization_id = $3 "
        "             ) as _in "
        "        where date >= {} "
        "          and date <= {} "
        "    ), "
        "    _viol as ( "
        "        select vi.log_id, count(vi.log_id) violation_count "
        "        from _raw, "
        "             violation vi "
        "        where vi.log_id = _raw.id "
        "           {} "  # filter
        "        group by vi.log_id "
        "    ), "
        "    _fin as ( "
        "        select *, dv.dvir_count, vi.violation_count "
        "        from _raw r, "
        "             _dvir as dv, "
        "             _viol as vi "
        "        where r.id = dv.log_id "
        "          and r.id = vi.log_id "
        "           {} "  # filter
        "           {} "  # filter
        "        limit $1 offset $2 "
        "    ), "
        "    _dvir as ( "
        "        select dv.log_id, count(dv.log_id) dvir_count "
        "        from _raw, "
        "             dvir dv "
        "        where dv.log_id = _raw.id "
        "         {} "  # filter
        "        group by dv.log_id "
        "    ), "
        "    tc as ( "
        "        select count(_fin.id) "
        "        from _fin "
        "    ) "
        "select *, (select tc.count from tc) count "
        "from _fin as _in, "
        "     drivers as d, "
        "     users as u, "
        "     vehicles as v "
        "where _in.driver_id = d.id "
        "  and d.user_id = u.id "
        "  and _in.vehicle_id = v.id "
        "order by {}; "

    ).format(start_date, end_date, violation_filter, driver_filter, vehicle_filter, dvir_filter, order_by)
    result = await db.list(query, tuple(args))
    for data in result:
        data['event_ids'] = json.loads(data['event_ids'])
        data['edited_event_ids'] = json.loads(data['edited_event_ids'])
        data['shipping_docs'] = json.loads(data['shipping_docs'])

    _data = {
        "data": result,
        "total_count": 0 if len(result) == 0 else result[0]['count']
    }
    return _data


async def db_get_by_date(org_id, start_date=datetime.now().date(),
                         end_date=datetime.now().date(),
                         **kwargs):
    query = """
        select _log_out.*,
        ev.id as event_id,
        log_id,
        start_datetime,
        duration,
        from_address,
        to_address,
        distance,
        ev.notes as event_notes,
        start_odometer,
        start_engine_hours,
        current_address,
        current_lon,
        current_lat,
        time_minute,
        event_status
        from (
             select distinct on (_log.id) _log.*
             from (
                  select *
                  from (
                       select *
                       from log
                       where organization_id = $1
                   ) as _in
                  where date >= $2 
                    and date <= $3
             ) as _log,
             violation as vi
             where vi.log_id = _log.id
               and vi.violation = $4
             ) as _log_out,
             events as ev
        where _log_out.id = ev.log_id
        order by date, time_minute;
    """
    result = await db.list(
        query,
        (org_id, start_date, end_date, kwargs.get("violation", ViolationName.MISSING_SIGNATURE))
    )
    for data in result:
        data['event_ids'] = json.loads(data['event_ids'])
        data['edited_event_ids'] = json.loads(data['edited_event_ids'])
        data['shipping_docs'] = json.loads(data['shipping_docs'])
    return result


pass


async def get_all(organization_id):
    result = await db.list("select * from log where organization_id = $1;", (organization_id,))
    for data in result:
        data['event_ids'] = json.loads(data['event_ids'])
        data['edited_event_ids'] = json.loads(data['edited_event_ids'])
        data['shipping_docs'] = json.loads(data['shipping_docs'])
    return result
