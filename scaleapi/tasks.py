from enum import Enum
from typing import List


class TaskType(Enum):
    """Task Type List"""

    Annotation = "annotation"
    Categorization = "categorization"
    Comparison = "comparison"
    CuboidAnnotation = "cuboidannotation"
    DataCollection = "datacollection"
    DocumentModel = "documentmodel"
    DocumentTranscription = "documenttranscription"
    ImageAnnotation = "imageannotation"
    LaneAnnotation = "laneannotation"
    LidarAnnotation = "lidarannotation"
    LidarLinking = "lidarlinking"
    LidarSegmentation = "lidarsegmentation"
    LidarTopdown = "lidartopdown"
    LineAnnotation = "lineannotation"
    NamedEntityRecognition = "namedentityrecognition"
    PointAnnotation = "pointannotation"
    PolygonAnnotation = "polygonannotation"
    SegmentAnnotation = "segmentannotation"
    Transcription = "transcription"
    TextCollection = "textcollection"
    VideoAnnotation = "videoannotation"
    VideoBoxAnnotation = "videoboxannotation"
    VideoPlaybackAnnotation = "videoplaybackannotation"
    VideoCuboidAnnotation = "videocuboidannotation"
    SensorFusion = "sensorfusion"
    Chat = "chat"
    ChatExperimental = "chatexperimental"
    ChatLite = "chatlite"
    MultiChat = "multichat"


class TaskReviewStatus(Enum):
    """Customer Audit Status of Task"""

    Accepted = "accepted"
    Fixed = "fixed"
    Commented = "commented"
    Rejected = "rejected"
    Pending = "pending"


class TaskStatus(Enum):
    """Status of Task"""

    Pending = "pending"
    Completed = "completed"
    Canceled = "canceled"


class Task:
    """Task class, containing task information."""

    def __init__(self, json, client):
        self._client = client
        self._json = json
        self.id = json["task_id"]

    def __getattr__(self, name):
        if name in self._json:
            return self._json[name]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute {name}")

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f"Task(id={self.id})"

    def __repr__(self):
        return f"Task({self._json})"

    def as_dict(self):
        """Returns object details as a dictionary

        `Task.as_dict()['params']`

        Returns:
            Dict with object content
        """
        return self._json

    def refresh(self):
        """Refreshes the task details."""
        self._json = self._client.get_task(self.id).as_dict()

    def cancel(self, clear_unique_id: bool = False):
        """Cancels the task"""
        self._client.cancel_task(self.id, clear_unique_id)

    def audit(self, accepted: bool, comments: str = None):
        """Submit an audit to a completed task"""
        self._client.audit_task(self.id, accepted, comments)

    def update_unique_id(self, unique_id: str):
        """Updates unique_id of a task"""
        self._client.update_task_unique_id(self.id, unique_id)

    def clear_unique_id(self):
        """Clears unique_id of a task"""
        self._client.clear_task_unique_id(self.id)

    def set_metadata(self, metadata: dict):
        """Sets the metadata of a task"""
        self._client.set_task_metadata(self.id, metadata)

    def set_tags(self, tags: List[str]):
        """Sets tags of a task"""
        self._client.set_task_tags(self.id, tags)

    def add_tags(self, tags: List[str]):
        """Adds tags for a task"""
        self._client.add_task_tags(self.id, tags)

    def delete_tags(self, tags: List[str]):
        """Sets tags for a task"""
        self._client.delete_task_tags(self.id, tags)
