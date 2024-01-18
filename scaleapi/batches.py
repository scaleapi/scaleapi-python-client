from enum import Enum


class BatchStatus(Enum):
    """Status of Batches"""

    Staging = "staging"
    InProgress = "in_progress"
    Completed = "completed"


class Batch:
    """Batch class, contains Batch information"""

    def __init__(self, json, client):
        self._json = json
        self.name = json["name"]
        self.status = json["status"]
        self.project = json["project"]
        self.created_at = json["created_at"]
        self.project = json["project"]
        self.metadata = json["metadata"]

        self.tasks_pending = None
        self.tasks_completed = None
        self.tasks_error = None
        self.tasks_canceled = None
        self._client = client

    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return f"Batch(name={self.name})"

    def __repr__(self):
        return f"Batch({self._json})"

    def as_dict(self):
        """Returns all attributes as a dictionary"""
        return self._json

    def finalize(self):
        """Finalizes the batch"""
        res = self._client.finalize_batch(self.name)
        self.status = res.status
        return res

    def get_status(self):
        """Returns status of the batch and
        updates tasks_... parameters
        """
        res = self._client.batch_status(self.name)
        self.status = res["status"]
        for stat in ["pending", "completed", "error", "canceled"]:
            setattr(self, "tasks_" + stat, res.get(stat, 0))
        return res
