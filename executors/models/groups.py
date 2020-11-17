import json


class Groups:
    id: int = 0
    name: str = ""
    note: str = ""
    units_count: int = 0
    units = {}
    organization_id: int = 0


    def __init__(self, data=None):
        if not data:
            data = {}
        self.deserialize(data)


    def deserialize(self, data):
        if not data:
            data = {}
        self.id = data.get("id", self.id)
        self.name = data.get("name", self.name)
        self.note = data.get("note", self.note)
        self.units_count = data.get("units_count", self.units_count)
        self.units = data.get("units", self.units)
        self.organization_id = data.get("organization_id", self.organization_id)


    def serialize(self):
        _data = {}
        _data['id'] = self.id
        _data['name'] = self.name
        _data['note'] = self.note
        _data['units_count'] = self.units_count
        _data['units'] = self.units
        _data['organization_id'] = self.organization_id
        return _data


    def to_json(self, data):
        return json.dumps(self.serialize())
