import json
from datetime import datetime


class Vehicle:
    id: int = 0
    make: str = ""
    model: str = ""
    year: datetime = datetime.now()
    license_plate_no: str = ""
    enter_vin_manually: bool = True
    vin: str = ""
    notes: str = ""
    eld_id: int = 0
    fuel_type_id: int = 0
    plate_issue_state_id: int = 0
    vehicle_id: str = ""
    status: int = 0
    organization_id: int = 0
    driver_id: int = 0

    fuel_type = {}
    plate_issue_state = {}
    eld = {}


    def __init__(self, data=None):
        if not data:
            data = {}
        self.deserialize(data)


    def deserialize(self, data):
        if not data:
            data = {}
        self.id = data.get("id", self.id)
        self.make = data.get("make", self.make)
        self.model = data.get("model", self.model)
        self.year = data.get("year", self.year)
        self.license_plate_no = data.get("license_plate_no", self.license_plate_no)
        self.enter_vin_manually = data.get("enter_vin_manually", self.enter_vin_manually)
        self.vin = data.get("vin", self.vin)
        self.notes = data.get("notes", self.notes)
        self.eld_id = data.get("eld_id", self.eld_id)
        self.fuel_type_id = data.get("fuel_type_id", self.fuel_type_id)
        self.plate_issue_state_id = data.get("plate_issue_state_id", self.plate_issue_state_id)
        self.vehicle_id = data.get("vehicle_id", self.vehicle_id)
        self.status = data.get("status", self.status)
        self.organization_id = data.get("organization_id", self.organization_id)
        self.fuel_type = data.get("fuel_type", self.fuel_type)
        self.plate_issue_state = data.get("plate_issue_state", self.plate_issue_state)
        self.eld = data.get("eld", self.eld)
        self.driver_id = data.get("driver_id", self.driver_id)


    def serialize(self):
        _data = {}
        for param, val in self.__dict__.items():
            _data[param] = val
        return _data


    def to_json(self, data):
        return json.dumps(self.serialize())
