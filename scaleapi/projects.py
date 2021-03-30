class Project:
    """Project class, containing Project information."""

    def __init__(self, json, client):
        self._json = json
        self.name = json["name"]
        self.type = json["type"]
        self._client = client
        self.params = None
        self.version = None
        self.instruction = None

        if len(json["param_history"]):
            self.params = json["param_history"][-1]
            self.version = self.params["version"]
            if "instruction" in self.params:
                self.instruction = self.params["instruction"]

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return f"Project(name={self.name})"

    def __repr__(self):
        return f"Project({self._json})"

    def as_dict(self):
        """Returns all attributes as a dictionary"""
        return self._json
