import json
from datetime import datetime


class Dvir:
    id: int = 0
    log_id: int = 0
    driver_id: int = 0
    vehicle_id: int = 0
    datetime: datetime = datetime.now()
    status_code: int = 0
    status_name: str = ""
    description: str = ""
    driver_signature: str = ""
    mechanic_signature: str = ""


    def __init__(self, data=None):
        if not data:
            data = {}
        self.deserialize(data)


    def deserialize(self, data):
        if not data:
            data = {}
        self.id = data.get("id", self.id)
        self.log_id = data.get("log_id", self.log_id)
        self.driver_id = data.get("driver_id", self.driver_id)
        self.vehicle_id = data.get("vehicle_id", self.vehicle_id)
        self.datetime = data.get("datetime", self.datetime)
        self.status_code = data.get("status_code", self.status_code)
        self.status_name = data.get("status_name", self.status_name)
        self.description = data.get("description", self.description)
        self.driver_signature = data.get("driver_signature", self.driver_signature)
        self.mechanic_signature = data.get("mechanic_signature", self.mechanic_signature)


    def serialize(self):
        _data = {}
        for param, val in self.__dict__.items():
            _data[param] = val
        return _data


    def to_json(self):
        return json.dumps(self.serialize())
