import json


class FuelType:
    id: int = 0
    title: str = ""
    alias: str = ""


    def __init__(self, data=None):
        if not data:
            data = {}
        self.deserialize(data)


    def deserialize(self, data):
        if not data:
            data = {}
        self.id = data.get("id", self.id)
        self.title = data.get("make", self.title)
        self.alias = data.get("model", self.alias)


    def serialize(self):
        _data = {}
        _data['id'] = self.id
        _data['title'] = self.title
        _data['alias'] = self.alias
        return _data


    def to_json(self, data):
        return json.dumps(self.serialize())
