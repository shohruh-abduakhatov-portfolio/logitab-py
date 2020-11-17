import json
from datetime import datetime


class Driver:
    id: int = 0
    driver_license_no: str = ""
    driver_code: str = ""
    co_driver_id: int = 0
    trailer_no: str = ""
    note: str = ""
    enable_for_elds: bool = True
    enable_for_elog: bool = False
    allow_yard_move: bool = False
    allow_personal_conveyance: bool = False
    activated_datetime: datetime = datetime.now()
    terminated_datetime: datetime = datetime.now()
    date_created: datetime = datetime.now()
    app_version: str = ""
    status: int = 1
    color: str = ""
    device_version_id: int = 0
    driver_license_issue_state_id: int = 0
    terminal_id: int = None
    vehicle_id: int = None
    user_id: int = None
    organization_id: int = None


    def __init__(self, data=None):
        if not data:
            data = {}
        self.deserialize(data)


    def deserialize(self, data):
        if not data:
            data = {}
        self.id = data.get("id", self.id)
        self.driver_license_no = data.get("driver_license_no", self.driver_license_no)
        self.driver_code = data.get("driver_code", self.driver_code)
        self.co_driver_id = data.get("co_driver_id", self.co_driver_id)
        self.trailer_no = data.get("trailer_no", self.trailer_no)
        self.note = data.get("note", self.note)
        self.enable_for_elds = data.get("enable_for_elds", self.enable_for_elds)
        self.enable_for_elog = data.get("enable_for_elog", self.enable_for_elog)
        self.allow_yard_move = data.get("allow_yard_move", self.allow_yard_move)
        self.allow_personal_conveyance = data.get("allow_personal_conveyance", self.allow_personal_conveyance)
        self.activated_datetime = data.get("activated_datetime", self.activated_datetime)
        self.terminated_datetime = data.get("terminated_datetime", self.terminated_datetime)
        self.date_created = data.get("terminated_datetime", self.terminated_datetime)
        self.app_version = data.get("app_version", self.app_version)
        self.status = data.get("status", self.status)
        self.color = data.get("color", self.color)
        self.device_version_id = data.get("device_version_id", self.device_version_id)
        self.driver_license_issue_state_id = data.get("driver_license_issue_state_id",
                                                      self.driver_license_issue_state_id)
        self.terminal_id = data.get("terminal_id", self.terminal_id)
        self.vehicle_id = data.get("vehicle_id", self.vehicle_id)
        self.user_id = data.get("user_id", self.user_id)
        self.organization_id = data.get("organization_id", self.organization_id)


    def serialize(self):
        _data = {}
        for param, val in self.__dict__.items():
            _data[param] = val
        return _data


    def to_json(self):
        return json.dumps(self.serialize())
