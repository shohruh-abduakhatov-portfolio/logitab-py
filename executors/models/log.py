import json
from datetime import datetime


class Log:
    id: int = 0
    date: datetime = datetime.now()
    edited_event_ids: json = {}
    event_ids: json = {}
    driver_id: int = 0
    vehicle_id: int = 0
    terminal_id: int = 0
    organization_id: int = 0
    break_time: int = 480
    driving: int = 660
    shift: int = 840
    cycle: int = 4200
    signature_url: str = ""
    notes: str = ""
    shipping_docs: str = ""
    current_edit_request_report_url: str = ""
    edited_edit_request_report_url: str = ""


    def __init__(self, data=None):
        if not data:
            data = {}
        self.deserialize(data)


    def deserialize(self, data):
        if not data:
            data = {}
        self.id = data.get("id", self.id)
        self.date = data.get("date", self.date)
        self.edited_event_ids = data.get("edited_event_ids", self.edited_event_ids)
        self.event_ids = data.get("event_ids", self.event_ids)
        self.driver_id = data.get("driver_id", self.driver_id)
        self.vehicle_id = data.get("vehicle_id", self.vehicle_id)
        self.terminal_id = data.get("terminal_id", self.terminal_id)
        self.organization_id = data.get("organization_id", self.organization_id)
        self.break_time = data.get("break", self.break_time)
        self.driving = data.get("driving", self.driving)
        self.shift = data.get("shift", self.shift)
        self.cycle = data.get("cycle", self.cycle)
        self.signature_url = data.get("signature_url", self.signature_url)
        self.notes = data.get("signature_url", self.signature_url)
        self.shipping_docs = data.get("signature_url", self.signature_url)
        self.current_edit_request_report_url = data.get("current_edit_request_report_url", self.current_edit_request_report_url)
        self.edited_edit_request_report_url = data.get("edited_edit_request_report_url", self.edited_edit_request_report_url)


    def serialize(self):
        _data = {}
        for param, val in self.__dict__.items():
            _data[param] = val
        return _data


    def to_json(self):
        return json.dumps(self.serialize())
