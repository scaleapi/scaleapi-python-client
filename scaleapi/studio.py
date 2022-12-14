from enum import Enum


class StudioLabelerAssignment:
    """Labeler Assignment class, contains information about
    assignments for labelers."""

    def __init__(self, assigned_projects, email, client):
        self._json = assigned_projects
        self._client = client
        self.email = email
        self.assigned_projects = assigned_projects

    def __hash__(self):
        return hash(self.email)

    def __str__(self):
        return (
            f"StudioLabelerAssignment(email={self.email},"
            f"assigned_projects={self.assigned_projects})"
        )

    def __repr__(self):
        return f"StudioLabelerAssignment({self._json})"

    def as_dict(self):
        """Returns all attributes as a dictionary"""
        return self._json


class StudioWorker:
    """Worker object that is returned in the 'workers' array."""

    def __init__(self, json, client):
        self._json = json
        self._client = client
        self.id = json["id"]
        self.email = json["email"]

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f"StudioWorker(id={self.email})"

    def __repr__(self):
        return f"StudioWorker({self._json})"

    def as_dict(self):
        """Returns all attributes as a dictionary"""
        return self._json


class StudioProjectGroup:
    """Studio project group."""

    def __init__(self, json, client):
        self._json = json
        self._client = client
        self.id = json["id"]
        self.name = json["name"]
        self.numWorkers = json["numWorkers"]
        self.isSingleton = json["isSingleton"]
        if json.get("workers"):
            self.workers = ([StudioWorker(w, client) for w in json["workers"]],)
        else:
            self.workers = []

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f"StudioProjectGroup(name={self.name})"

    def __repr__(self):
        return f"StudioProjectGroup({self._json})"

    def as_dict(self):
        """Returns all attributes as a dictionary"""
        return self._json


class StudioBatchStatus(Enum):
    """Studio Batch Statuses"""

    Production = "Production"


class StudioBatch:
    """Studio Batch"""

    def __init__(self, json, client):
        self._json = json
        self._client = client
        self.id = json["id"]
        self.name = json["name"]
        self.project_id = json["projectId"]
        self.project_name = json["projectName"]
        self.batch_type = json["batchType"]
        self.studio_priority = json.get("studioPriority")
        self.total = json["total"]
        self.completed = json["completed"]
        self.groups = json["groups"]

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f"StudioBatch(name={self.name})"

    def __repr__(self):
        return f"StudioBatch({self._json})"

    def as_dict(self):
        """Returns all attributes as a dictionary"""
        return self._json
