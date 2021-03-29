from enum import Enum


class TaskType(Enum):
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


class TaskReviewStatus(Enum):
    Accepted = "accepted"
    Fixed = "fixed"
    Commented = "commented"
    Rejected = "rejected"


class TaskStatus(Enum):
    Pending = "pending"
    Completed = "completed"
    Canceled = "canceled"


class Task(object):
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
        """Refreshes the task details.
        """
        self._json = self._client.fetch_task(self.id).as_dict()

    def cancel(self):
        """Cancels the task
        """
        self._client.cancel_task(self.id)
