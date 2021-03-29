class Project(object):
    def __init__(self, json, client):
        self._json = json
        self.name = json["name"]
        self.type = json["type"]
        self._client = client

        if len(json["param_history"]):
            self.version = json["param_history"][-1]["version"]
            self.instruction = json["param_history"][-1]["instruction"]

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return f"Project(name={self.name})"

    def __repr__(self):
        return f"Project({self._json})"

    def as_dict(self):
        return self._json
