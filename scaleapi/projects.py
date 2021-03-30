class Project:
    """Project class, containing Project information."""

    def __init__(self, json, client):
        self._json = json
        self.name = json["name"]
        self.type = json["type"]
        self._client = client

        if len(json["param_history"]):
            last_params = json["param_history"][-1]
            self.version = last_params["version"]
            if "instruction" in last_params:
                self.instruction = last_params["instruction"]

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return f"Project(name={self.name})"

    def __repr__(self):
        return f"Project({self._json})"

    def as_dict(self):
        """Returns all attributes as a dictionary"""
        return self._json
