import datetime
import json
from functools import partial

from marshmallow import Schema, fields
from marshmallow.validate import Range

from modules.core.Boolean import Boolean
from modules.core.Date2 import Date2
from modules.core.DateTime import DateTime


class DriverSchema(Schema):
    id = fields.Int(required=False)
    driver_license_no = fields.Str(required=True)
    co_driver_id = fields.Int(required=False)
    trailer_no = fields.Str(required=False)
    note = fields.Str(required=False)
    enable_for_elds = fields.Bool(required=False)
    enable_for_elog = fields.Bool(required=False)
    allow_yard_move = fields.Bool(required=False)
    allow_personal_conveyance = fields.Bool(required=False)
    activated_datetime = fields.DateTime(required=False, allow_none=True)
    terminated_datetime = fields.DateTime(required=False, allow_none=True)
    app_version = fields.Str(required=False)
    color = fields.Str(required=False)
    status = fields.Int(required=True)
    device_version_id = fields.Int(required=False)
    driver_license_issue_state_id = fields.Int(required=True)
    terminal_id = fields.Int(required=True)
    vehicle_id = fields.Int(required=True)
    user_id = fields.Int(required=False)
    driver_code = fields.Str(required=True)
    date_created = fields.DateTime(required=False, default=datetime.datetime.now())
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    email = fields.Email(required=True)
    phone = fields.Str(required=True)


class DriverEditSchema(DriverSchema):
    driver_license_no = fields.Str(required=False)
    app_version = fields.Str(required=False)
    status = fields.Int(required=False)
    device_version_id = fields.Int(required=False)
    driver_license_issue_state_id = fields.Int(required=False)
    terminal_id = fields.Int(required=False)
    vehicle_id = fields.Int(required=False)
    driver_code = fields.Str(required=False)
    first_name = fields.Str(required=False)
    last_name = fields.Str(required=False)
    username = fields.Str(required=False)
    password = fields.Str(required=False)
    email = fields.Email(required=False)
    phone = fields.Str(required=False)


class DriverListSchema(Schema):
    data = fields.Nested(DriverSchema(many=True))


class TerminalSchema(Schema):
    id = fields.Int(required=False)
    name = fields.Str(required=True)
    state_id = fields.Int(required=True)
    home_terminal_address = fields.Str(required=True)
    home_terminal_timezone_id = fields.Int(required=True, validate=[Range(min=1)])


class TerminalEditSchema(TerminalSchema):
    name = fields.Str(required=False)
    state_id = fields.Int(required=False)
    home_terminal_address = fields.Str(required=False)
    home_terminal_timezone_id = fields.Int(required=False, validate=[Range(min=1)])


class TerminalListSchema(Schema):
    data = fields.Nested(TerminalSchema(many=True))


class VehicleSchema(Schema):
    id = fields.Int(ired=False)
    vehicle_id = fields.Str(required=True)
    make = fields.Str(required=True)
    model = fields.Str(required=True)
    year = fields.Date(required=True)
    license_plate_no = fields.Str(required=True)
    plate_issue_state_id = fields.Int(required=True)
    enter_vin_manually = fields.Bool(default=False)
    vin = fields.Str(required=True)
    eld_id = fields.Int(required=False)
    notes = fields.Str(required=False)
    fuel_type_id = fields.Int(required=True)
    status = fields.Int(required=False)


class VehicleEditSchema(VehicleSchema):
    vehicle_id = fields.Str(required=False)
    make = fields.Str(required=False)
    model = fields.Str(required=False)
    year = fields.Date(required=False)
    license_plate_no = fields.Str(required=False)
    plate_issue_state_id = fields.Int(required=False)
    vin = fields.Str(required=False)
    fuel_type_id = fields.Int(required=False)


class VehicleListSchema(Schema):
    data = fields.Nested(VehicleSchema(many=True))


class DrivingEventSchema(Schema):
    id = fields.Int(required=False)
    log_id = fields.Int(required=False)
    driver_id = fields.Int(required=True)
    vehicle_id = fields.Int(required=True)
    unit_id = fields.Int(required=True)
    start_datetime = fields.DateTime(required=True)
    duration = fields.Int()
    from_address = fields.Str()
    to_address = fields.Str()
    distance = fields.Float()
    start_odometer = fields.Float()
    start_engine_hours = fields.Float()
    notes = fields.Str(required=False)
    current_lon = fields.Float()
    current_lat = fields.Float()
    current_address = fields.Str()
    event_status = fields.Str(required=True)
    time_minute = fields.Int()


class DrivingEditEventSchema(DrivingEventSchema):
    driver_id = fields.Int(required=False)
    log_id = fields.Int(required=False)
    vehicle_id = fields.Int(required=False)
    unit_id = fields.Int(required=False)
    start_datetime = fields.DateTime(required=False)
    event_status = fields.Str(required=False)


class DrivingEventListSchema(Schema):
    data = fields.Nested(DrivingEventSchema(many=True))


class EventSchema(Schema):
    id = fields.Int(required=False)
    log_id = fields.Int(required=False)
    driver_id = fields.Int(required=True)
    vehicle_id = fields.Int(required=True)
    unit_id = fields.Int(required=True)
    start_datetime = fields.DateTime(required=True)
    duration = fields.Int()
    from_address = fields.Str()
    to_address = fields.Str()
    distance = fields.Float()
    start_odometer = fields.Float()
    start_engine_hours = fields.Float()
    notes = fields.Str(required=False)
    current_lon = fields.Float()
    current_lat = fields.Float()
    current_address = fields.Str()
    event_status = fields.Str(required=True)
    time_minute = fields.Int()


class EditedEventSchema(EventSchema):
    edited_datetime = fields.DateTime(default=datetime.datetime.now())
    edited_status_code = fields.Int()
    edited_status_desc = fields.Str()


class EditedEventListSchema(Schema):
    data = fields.Nested(EditedEventSchema(many=True))


class EditedAndCurrentEvent(Schema):
    current_event = fields.Nested(EventSchema())
    edited_event = fields.Nested(EditedEventSchema())


class EventEditSchema(EventSchema):
    driver_id = fields.Int(required=False)
    log_id = fields.Int(required=False)
    vehicle_id = fields.Int(required=False)
    unit_id = fields.Int(required=False)
    start_datetime = fields.DateTime(required=False)
    event_status = fields.Str(required=False)


class EventListSchema(Schema):
    data = fields.Nested(EventSchema(many=True))


class UnitSchema(Schema):
    id = fields.Int(required=False)
    notes = fields.Str(required=False)
    icon = fields.Str(required=False)
    driver_id = fields.Int(required=True)
    vehicle_id = fields.Int(required=True)
    groups = fields.Dict(required=False)
    # groups = fields.List(required=False, default=[])


class UnitEditSchema(UnitSchema):
    driver_id = fields.Int(required=False)
    vehicle_id = fields.Int(required=False)


class UnitListSchema(Schema):
    data = fields.Nested(UnitSchema(many=True))


class EldSchema(Schema):
    id = fields.Int(required=False)
    serial_no = fields.Str(required=True)
    device_version = fields.Str(required=False)
    telematics = fields.Str(required=False)
    notes = fields.Str(required=False)


class EldEditSchema(EldSchema):
    serial_no = fields.Str(required=False)


class EldListSchema(Schema):
    data = fields.Nested(EldSchema(many=True))


class GroupSchema(Schema):
    id = fields.Int(required=False)
    name = fields.Str(required=True)
    note = fields.Str(required=False)
    units_count = fields.Int(required=False)
    units = fields.Dict(required=False)


class GroupEditSchema(GroupSchema):
    name = fields.Str(required=False)


class GroupListSchema(Schema):
    data = fields.Nested(GroupSchema(many=True))


class FuelType(Schema):
    id = fields.Int(required=False)
    title = fields.Str(required=True)
    alias = fields.Str(required=True)


class FuelTypeListSchema(Schema):
    data = fields.Nested(FuelType(many=True))


class IssueState(Schema):
    id = fields.Int(required=False)
    title = fields.Str(required=True)
    alias = fields.Str(required=True)


class IssueStateListSchema(Schema):
    data = fields.Nested(FuelType(many=True))


class LogSchema(Schema):
    id = fields.Int(required=False)
    date = fields.DateTime(required=False)
    edited_event_ids = fields.Dict(required=False)
    event_ids = fields.Dict(required=False)
    driver_id = fields.Int(required=False)
    vehicle_id = fields.Int(required=False)
    terminal_id = fields.Int(required=False)
    organization_id = fields.Int(required=False)
    break_time = fields.Int(required=False)
    driving = fields.Int(required=False)
    shift = fields.Int(required=False)
    cycle = fields.Int(required=False)
    signature_url = fields.Dict(required=False)
    notes = fields.Dict(required=False)
    shipping_docs = fields.Dict(required=False)
    current_edit_request_report_url = fields.Dict(required=False)
    edited_edit_request_report_url = fields.Dict(required=False)


def default_json(obj):
    if isinstance(obj, datetime.datetime) or isinstance(obj, DateTime) or \
            isinstance(obj, datetime.date) or isinstance(obj, Date2):
        return str(obj)
    elif isinstance(obj, Boolean) or isinstance(obj, datetime.datetime):
        return obj.value.value == 1

    raise TypeError('Unable to serialize {!r}'.format(obj))


custom_dumps = partial(json.dumps, default=default_json)

driver_schema = DriverSchema()
driver_edit_schema = DriverEditSchema()

terminal_schema = TerminalSchema()
terminal_edit_schema = TerminalEditSchema()

unit_schema = UnitSchema()
unit_edit_schema = UnitEditSchema()

driving_event_schema = DrivingEventSchema()
driving_event_edit_schema = DrivingEditEventSchema()

event_schema = EventSchema()
event_edit_schema = EventEditSchema()

edited_event_schema = EditedEventSchema()

vehicle_schema = VehicleSchema()
vehicle_edit_schema = VehicleEditSchema()

eld_schema = EldSchema()
eld_edit_schema = EldEditSchema()

group_schema = GroupSchema()
group_edit_schema = GroupEditSchema()
