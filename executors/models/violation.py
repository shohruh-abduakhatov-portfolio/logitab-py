import json


class Violation:
    id: int = 0
    log_id: int = 0
    violation: str = ""
    name: str = ""
    description: str = ""
    error_level_code: int = 0
    error_level_desc: str = ""
    object_name: str = ""
    field_name: str = ""


    def __init__(self, data=None):
        if not data:
            data = {}
        self.deserialize(data)


    def deserialize(self, data):
        if not data:
            data = {}
        self.id = data.get("id", self.id)
        self.log_id = data.get("log_id", self.log_id)
        self.violation = data.get("violation", self.violation)
        self.name = data.get("name", self.name)
        self.description = data.get("description", self.description)
        self.error_level_code = data.get("error_level_code", self.error_level_code)
        self.error_level_desc = data.get("error_level_desc", self.error_level_desc)
        self.object_name = data.get("object_name", self.object_name)
        self.field_name = data.get("field_name", self.field_name)


    def serialize(self):
        _data = {
            'id': self.id,
            'log_id': self.log_id,
            'violation': self.violation,
            'name': self.name,
            'description': self.description,
            'error_level_code': self.error_level_code,
            'error_level_desc': self.error_level_desc,
            'object_name': self.object_name,
            'field_name': self.field_name
        }
        return _data


    def to_json(self):
        return json.dumps(self.serialize())
