import json


class Units:
    id: int = 0
    notes: str = ""
    icon: str = ""
    driver_id: int = 0
    vehicle_id: int = 0
    groups: dict = {}
    vehicle: dict = {}
    driver: dict = {}


    def __init__(self, data=None):
        if not data:
            data = {}
        self.deserialize(data)


    def deserialize(self, data):
        if not data:
            data = {}
        self.id = data.get("id", self.id)
        self.notes = data.get("notes", self.notes)
        self.icon = data.get("icon", self.icon)
        self.driver_id = data.get("driver_id", self.driver_id)
        self.vehicle_id = data.get("vehicle_id", self.vehicle_id)
        self.groups = data.get("groups", self.groups)


    def serialize(self):
        _data = {}
        for param, val in self.__dict__.items():
            _data[param] = val
        return _data


    def to_json(self):
        return json.dumps(self.serialize())
