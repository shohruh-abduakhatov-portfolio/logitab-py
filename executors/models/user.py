import json
from datetime import datetime


class User:
    id: int = 0
    username: str = ""
    password: str = ""
    role: str = ""
    date_created: datetime = datetime.now()
    organization_id: int = 0
    first_name: str = ""
    last_name: str = ""
    status: bool = False
    phone: str = ""
    email: str = ""


    def __init__(self, data=None):
        if not data:
            data = {}
        self.deserialize(data)


    def deserialize(self, data):
        if not data:
            data = {}
        self.id = data.get("id", self.id)
        self.username = data.get("username", self.username)
        self.password = data.get("password", self.password)
        self.role = data.get("role", self.role)
        self.date_created = data.get("date_created", self.date_created)
        self.organization_id = data.get("organization_id") or data.get("organisation_id", self.organization_id)

        self.first_name = data.get("first_name", self.first_name)
        self.last_name = data.get("last_name", self.last_name)
        self.status = data.get("status", self.status)
        self.phone = data.get("phone", self.phone)
        self.email = data.get("email", self.email)


    def serialize(self):
        _data = {}
        _data['id'] = self.id
        _data['username'] = self.username
        _data['password'] = self.password
        _data['role'] = self.role
        _data['date_created'] = self.date_created
        _data['organization_id'] = self.organization_id
        _data['first_name'] = self.first_name
        _data['last_name'] = self.last_name
        _data['status'] = self.status
        _data['phone'] = self.phone
        _data['email'] = self.email
        return _data


    def to_json(self):
        return json.dumps(self.serialize())
