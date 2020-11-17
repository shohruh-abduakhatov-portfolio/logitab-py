class Param:
    _stack = []


    def __init__(self):
        self._stack = []


    def paginate(self):
        self._stack += [{
            'in': 'query',
            'name': 'limit',
            'schema': {'type': 'int'},
        }, {
            'in': 'query',
            'name': 'offset',
            'schema': {'type': 'int'},
        }]
        return self


    def query(self, name="", type="string"):
        self._stack.append({
            'in': 'query',
            'name': name,
            'schema': {'type': type},
        })
        return self


    def query_req(self, name="", type="string"):
        self._stack.append({
            'in': 'query',
            'name': name,
            'schema': {'type': type},
            "required": 'true',
        })
        return self


    def url_path(self, name: str, type="string"):
        self._stack.append({
            "in": "path",
            "name": name,
            "required": 'true',
            "type": type,
        })
        return self


    def header(self, name: str, type="string", req='true'):
        self._stack.append({
            "in": "header",
            "name": name,
            "required": req,
            "type": type,
        })
        return self


    def build(self) -> list:
        return self._stack
