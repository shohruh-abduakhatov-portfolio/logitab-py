import json
from datetime import datetime

from executors.utils.enum import EventEditedCodeEnum, EventEditedDescEnum


class EditedEvent:
    id: int = 0
    log_id: int = 0
    start_datetime: datetime = datetime.now()
    start_odometer: float = 0.
    start_engine_hours: float = 0.
    duration: int = 0
    from_address: str = ""
    to_address: str = ""
    distance: int = 0
    notes: str = ""
    driver_id: int = 0
    unit_id: int = 0
    vehicle_id: int = 0
    organization_id: int = 0
    # new added
    current_address: str = ""
    current_lon: float = 0.
    current_lat: float = 0.
    time_minute: int = 0
    event_status: str = 'off'
    # 2nd added
    edited_datetime: datetime = datetime.now()
    edited_status_code: int = EventEditedCodeEnum.WAITING
    edited_status_desc: str = EventEditedDescEnum.WAITING


    # deleted end_odo and end_engine_h

    def __init__(self, data=None):
        if not data:
            data = {}
        self.deserialize(data)


    def deserialize(self, data):
        if not data:
            data = {}
        self.id = data.get("id", self.id)
        self.log_id = data.get("log_id", self.log_id)
        self.start_datetime = data.get("start_datetime", self.start_datetime)
        self.start_odometer = data.get("start_odometer", self.start_odometer)
        self.start_engine_hours = data.get("start_engine_hours", self.start_engine_hours)
        self.duration = data.get("duration", self.duration)
        self.from_address = data.get("from_address", self.from_address)
        self.to_address = data.get("to_address", self.to_address)
        self.distance = data.get("distance", self.distance)
        self.notes = data.get("notes", self.notes)
        self.driver_id = data.get("driver_id", self.driver_id)
        self.unit_id = data.get("unit_id", self.unit_id)
        self.vehicle_id = data.get("vehicle_id", self.vehicle_id)
        self.organization_id = data.get("organization_id", self.organization_id)
        self.current_address = data.get("current_address", self.current_address)
        self.current_lon = data.get("current_lon", self.current_lon)
        self.current_lat = data.get("current_lat", self.current_lat)
        self.time_minute = data.get("time_minute", self.time_minute)
        self.event_status = data.get("event_status", self.event_status)
        self.edited_datetime = data.get("edited_datetime", self.edited_datetime)
        self.edited_status_code = data.get("edited_status_code", self.edited_status_code)
        self.edited_status_desc = data.get("edited_status_desc", self.edited_status_desc)


    def serialize(self):
        _data = {}
        for param, val in self.__dict__.items():
            _data[param] = val
        return _data


    def to_json(self):
        return json.dumps(self.serialize())
