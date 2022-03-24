class TrainingTask:
    """TrainingTask class, containing TrainingTask information."""

    def __init__(self, json, client):
        self._json = json
        self.id = json["id"]
        self.initial_response = getattr(json, "initial_response", None)
        self.expected_response = json["expected_response"]
        self._client = client

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f"TrainingTask(id={self.id})"

    def __repr__(self):
        return f"TrainingTask({self._json})"

    def as_dict(self):
        """Returns all attributes as a dictionary"""
        return self._json
