from enum import Enum
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

SensorId = Union[str, int]
Frames = Union[int, Tuple[int, int]]


class AuditResult(Enum):
    """Overall outcome of a fixless audit"""

    Accepted = "accepted"
    Rejected = "rejected"


class FeedbackItemType(Enum):
    """Kind of feedback item"""

    Comment = "comment"
    Confirmation = "confirmation"
    Error = "error"
    Flag = "flag"


class ErrorCategory(Enum):
    """Category of an error feedback item"""

    Attribute = "attribute"
    Extraneous = "extraneous"
    Geometry = "geometry"
    Label = "label"
    Missing = "missing"
    Position = "position"


class Severity(Enum):
    """Severity of an error feedback item"""

    Mild = "mild"
    Standard = "standard"
    Severe = "severe"


def _frame_range(frames: Frames) -> Dict[str, Any]:
    start, end = (frames, frames) if isinstance(frames, int) else frames
    return {"type": "frame_range", "start": start, "end": end}


class Scope:
    """Where in the task's response a feedback item applies.

    Build one with the class methods, e.g.
    `Scope.annotation("cuboid_1", frames=(0, 12))`.
    `frames` is a single frame index or an inclusive (start, end) range.
    The API validates scopes; invalid ones raise ScaleInvalidRequest.
    """

    def __init__(self, scope_type: str, frames: Frames, **fields):
        self.type = scope_type
        self._json = {
            "type": scope_type,
            "interval": _frame_range(frames),
            **{k: v for k, v in fields.items() if v is not None},
        }

    @classmethod
    def annotation(
        cls,
        annotation_id: str,
        frames: Frames,
        sensor_id: Optional[SensorId] = None,
        attribute: Optional[str] = None,
    ) -> "Scope":
        """An existing annotation, optionally one of its attributes"""
        return cls(
            "annotation",
            frames,
            annotation_id=annotation_id,
            sensor_id=sensor_id,
            attribute=attribute,
        )

    @classmethod
    def scene(
        cls,
        frames: Frames,
        sensor_id: Optional[SensorId] = None,
        attribute: Optional[str] = None,
    ) -> "Scope":
        """The whole scene, optionally one of its attributes"""
        return cls("scene", frames, sensor_id=sensor_id, attribute=attribute)

    @classmethod
    def point(
        cls,
        coordinates: Sequence[float],
        frames: Frames,
        sensor_id: Optional[SensorId] = None,
        missing_annotation_type: Optional[str] = None,
        missing_annotation_class: Optional[str] = None,
        stationary: Optional[bool] = None,
    ) -> "Scope":
        """A location [x, y], typically of a missing annotation"""
        return cls(
            "point",
            frames,
            coordinates=list(coordinates),
            sensor_id=sensor_id,
            missing_annotation_type=missing_annotation_type,
            missing_annotation_class=missing_annotation_class,
            stationary=stationary,
        )

    @classmethod
    def polygon(
        cls,
        vertices: Sequence[Sequence[float]],
        frames: Frames,
        sensor_id: Optional[SensorId] = None,
        missing_annotation_type: Optional[str] = None,
        missing_annotation_class: Optional[str] = None,
        stationary: Optional[bool] = None,
    ) -> "Scope":
        """A region [[x0, y0], [x1, y1], ...] of 3+ vertices"""
        return cls(
            "polygon",
            frames,
            vertices=[list(v) for v in vertices],
            sensor_id=sensor_id,
            missing_annotation_type=missing_annotation_type,
            missing_annotation_class=missing_annotation_class,
            stationary=stationary,
        )

    @classmethod
    def lss(
        cls,
        sensor_id: SensorId,
        anchor_point_id: int,
        frames: Frames,
        annotation_id: Optional[str] = None,
        correct_class: Optional[str] = None,
        estimated_points: Optional[float] = None,
        missing_annotation_type: Optional[str] = None,
        missing_annotation_class: Optional[str] = None,
    ) -> "Scope":
        """A picked point in a lidar segmentation (LSS) response"""
        return cls(
            "lss",
            frames,
            sensor_id=sensor_id,
            anchor_point_id=anchor_point_id,
            annotation_id=annotation_id,
            correct_class=correct_class,
            estimated_points=estimated_points,
            missing_annotation_type=missing_annotation_type,
            missing_annotation_class=missing_annotation_class,
        )

    def as_dict(self) -> Dict[str, Any]:
        """Returns the scope as sent to the API"""
        return self._json

    def __repr__(self):
        return f"Scope({self._json})"


class FeedbackItem:
    """A single piece of feedback in a fixless audit.

    Build one with the class methods, e.g.
    `FeedbackItem.error(scope, ErrorCategory.Geometry)`.
    """

    def __init__(
        self,
        item_type: FeedbackItemType,
        scope: Scope,
        description: Optional[str] = None,
        category: Optional[ErrorCategory] = None,
        severity: Optional[Severity] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.type = item_type
        self.scope = scope
        self.description = description
        self.category = category
        self.severity = severity
        self.metadata = metadata

    @classmethod
    def error(
        cls,
        scope: Scope,
        category: ErrorCategory,
        # Severity weights how much the error counts against the task's
        # score. The API requires one on every error; Standard is the
        # baseline weight, so pass Mild or Severe only to deviate.
        severity: Severity = Severity.Standard,
        description: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> "FeedbackItem":
        """An error in the response; counts against the task's score"""
        return cls(
            FeedbackItemType.Error, scope, description, category, severity, metadata
        )

    @classmethod
    def comment(
        cls,
        scope: Scope,
        description: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> "FeedbackItem":
        """A note that does not affect the task's score"""
        return cls(FeedbackItemType.Comment, scope, description, metadata=metadata)

    @classmethod
    def confirmation(
        cls,
        scope: Scope,
        description: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> "FeedbackItem":
        """Confirms that the scoped part of the response is correct"""
        return cls(FeedbackItemType.Confirmation, scope, description, metadata=metadata)

    @classmethod
    def flag(
        cls,
        scope: Scope,
        description: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> "FeedbackItem":
        """Flags the scoped part of the response for follow-up"""
        return cls(FeedbackItemType.Flag, scope, description, metadata=metadata)

    def as_dict(self) -> Dict[str, Any]:
        """Returns the feedback item as sent to the API"""
        item = {"type": self.type.value, "scope": self.scope.as_dict()}
        if self.category is not None:
            item["category"] = self.category.value
        if self.severity is not None:
            item["severity"] = self.severity.value
        if self.description is not None:
            item["description"] = self.description
        if self.metadata is not None:
            item["metadata"] = self.metadata
        return item

    def __repr__(self):
        return f"FeedbackItem({self.as_dict()})"


def build_fixless_audit_payload(
    task_id: str,
    target_response_url: str,
    accepted: bool,
    feedback_items: Optional[List[FeedbackItem]] = None,
    comments: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Builds the request body for `PUT /v1/audits`"""
    result = AuditResult.Accepted if accepted else AuditResult.Rejected
    payload: Dict[str, Any] = {
        "type": "fixless",
        "result": result.value,
        "task_id": task_id,
        "target_response_url": target_response_url,
        "feedback_items": [item.as_dict() for item in feedback_items or []],
    }
    optional = {"comments": comments, "metadata": metadata}
    payload.update({k: v for k, v in optional.items() if v is not None})
    return payload


class Audit:
    """Audit class, containing audit information."""

    def __init__(self, json, client):
        self._client = client
        self._json = json
        self.id = json["id"]

    def __getattr__(self, name):
        if name in self._json:
            return self._json[name]
        raise AttributeError(f"'{type(self).__name__}' object has no attribute {name}")

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f"Audit(id={self.id})"

    def __repr__(self):
        return f"Audit({self._json})"

    def as_dict(self):
        """Returns object details as a dictionary"""
        return self._json
