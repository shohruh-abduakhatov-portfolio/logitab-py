import json
from datetime import datetime

from executors.utils.enum import EditRequestHistoryDescEnum, EditRequestHistoryCodeEnum


class EditRequestHistory:
    id: int = 0
    log_id: int = 0
    created_datetime: datetime = datetime.now()
    status_name: int = EditRequestHistoryCodeEnum.WAITING
    status_desc: str = EditRequestHistoryDescEnum.WAITING


    def __init__(self, data=None):
        if not data:
            data = {}
        self.deserialize(data)


    def deserialize(self, data):
        if not data:
            data = {}
        self.id = data.get("id", self.id)
        self.log_id = data.get("log_id", self.log_id)
        self.created_datetime = data.get("created_datetime", self.created_datetime)
        self.status_name = data.get("status_name", self.status_name)
        self.status_desc = data.get("status_desc", self.status_desc)


    def serialize(self):
        _data = {}
        for param, val in self.__dict__.items():
            _data[param] = val
        return _data


    def to_json(self):
        return json.dumps(self.serialize())
