import json


class Eld:
    id: int = 0
    serial_no: str = ""
    device_version: str = ""
    telematics: str = ""
    notes: str = ""
    organization_id: int = 0


    def __init__(self, data=None):
        if not data:
            data = {}
        self.deserialize(data)


    def deserialize(self, data):
        if not data:
            data = {}
        self.id = data.get("id", self.id)
        self.serial_no = data.get("serial_no", self.serial_no)
        self.device_version = data.get("device_version", self.device_version)
        self.telematics = data.get("telematics", self.telematics)
        self.notes = data.get("notes", self.notes)
        self.organization_id = data.get("organization_id", self.organization_id)


    def serialize(self):
        _data = {}
        _data['id'] = self.id
        _data['serial_no'] = self.serial_no
        _data['device_version'] = self.device_version
        _data['telematics'] = self.telematics
        _data['notes'] = self.notes
        _data['organization_id'] = self.organization_id
        return _data


    def to_json(self, data):
        return json.dumps(self.serialize())
