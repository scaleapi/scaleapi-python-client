class TaskTemplate:
    """Task Template Object."""

    def __init__(self, json, client):
        self._json = json
        self._client = client
        self.id = json["id"]
        self.version = json["version"]
        self.created_at = json["created_at"]
        self.updated_at = json["updated_at"]
        self.template_variables = json["template_variables"]

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f"TaskTemplate(id={self.id})"

    def __repr__(self):
        return f"TaskTemplate({self._json})"

    def get_template_variables(self):
        """Returns template variables dictionary"""
        return self.template_variables

    def as_dict(self):
        """Returns task template object as JSON dictionary"""
        return self._json


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

    def get_template(self) -> TaskTemplate:
        """Returns TaskTemplate.
        Only works for Chat and TextCollection type."""
        return self._client.get_project_template(self.name)

    def as_dict(self):
        """Returns all attributes as a dictionary"""
        return self._json
