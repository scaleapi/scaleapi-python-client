# pylint: disable=missing-function-docstring
from unittest import mock

import scaleapi
from scaleapi.api import Api
from scaleapi.audits import (
    Audit,
    ErrorCategory,
    FeedbackItem,
    Scope,
    Severity,
    build_fixless_audit_payload,
)
from scaleapi.tasks import Task

RESPONSE_URL = "https://scaleapi-results.s3.amazonaws.com/annotations.json"


def test_scope_frames():
    assert Scope.scene(frames=3).as_dict()["interval"] == {
        "type": "frame_range",
        "start": 3,
        "end": 3,
    }
    assert Scope.annotation("a", frames=(0, 9)).as_dict() == {
        "type": "annotation",
        "annotation_id": "a",
        "interval": {"type": "frame_range", "start": 0, "end": 9},
    }


def test_error_item_defaults_and_serialization():
    item = FeedbackItem.error(
        Scope.annotation("cuboid_1", frames=(0, 4), sensor_id=0),
        ErrorCategory.Geometry,
        description="too loose",
    )
    assert item.as_dict() == {
        "type": "error",
        "scope": {
            "type": "annotation",
            "annotation_id": "cuboid_1",
            "sensor_id": 0,
            "interval": {"type": "frame_range", "start": 0, "end": 4},
        },
        "category": "geometry",
        "severity": "standard",
        "description": "too loose",
    }


def test_non_error_items_omit_category_and_severity():
    assert FeedbackItem.comment(Scope.scene(frames=0), "dark").as_dict() == {
        "type": "comment",
        "scope": {
            "type": "scene",
            "interval": {"type": "frame_range", "start": 0, "end": 0},
        },
        "description": "dark",
    }


def test_build_payload_omits_unset_fields():
    assert build_fixless_audit_payload("t1", RESPONSE_URL, accepted=True) == {
        "type": "fixless",
        "result": "accepted",
        "task_id": "t1",
        "target_response_url": RESPONSE_URL,
        "feedback_items": [],
    }
    payload = build_fixless_audit_payload(
        "t1",
        RESPONSE_URL,
        accepted=False,
        feedback_items=[
            FeedbackItem.error(
                Scope.annotation("a", frames=0), ErrorCategory.Label, Severity.Severe
            )
        ],
        comments="see items",
    )
    assert payload["result"] == "rejected"
    assert payload["comments"] == "see items"
    assert payload["feedback_items"][0]["severity"] == "severe"
    assert "metadata" not in payload


def test_client_create_fixless_audit_sends_put():
    client = scaleapi.ScaleClient("test_dummy", "pytest")
    with mock.patch.object(
        client.api, "put_request", return_value={"id": "audit_1", "result": "accepted"}
    ) as put:
        audit = client.create_fixless_audit(
            "t1", RESPONSE_URL, accepted=True, comments="ok"
        )
    put.assert_called_once_with(
        "audits",
        body={
            "type": "fixless",
            "result": "accepted",
            "task_id": "t1",
            "target_response_url": RESPONSE_URL,
            "feedback_items": [],
            "comments": "ok",
        },
    )
    assert audit.id == "audit_1"
    assert audit.result == "accepted"


def test_client_get_audit():
    client = scaleapi.ScaleClient("test_dummy", "pytest")
    with mock.patch.object(
        client.api, "get_request", return_value={"id": "audit_1", "type": "fixless"}
    ) as get:
        audit = client.get_audit("audit_1")
    get.assert_called_once_with("audit/audit_1")
    assert isinstance(audit, Audit)
    assert audit.id == "audit_1"
    assert audit.type == "fixless"


def test_client_get_task_audits():
    client = scaleapi.ScaleClient("test_dummy", "pytest")
    with mock.patch.object(
        client.api, "get_request", return_value=[{"id": "audit_2"}, {"id": "audit_1"}]
    ) as get:
        audits = client.get_task_audits("t1")
    get.assert_called_once_with("audits/task/t1")
    assert all(isinstance(audit, Audit) for audit in audits)
    assert [audit.id for audit in audits] == ["audit_2", "audit_1"]


def test_client_get_task_audits_empty():
    client = scaleapi.ScaleClient("test_dummy", "pytest")
    with mock.patch.object(client.api, "get_request", return_value=[]):
        assert client.get_task_audits("t1") == []


def test_task_methods_forward_to_client():
    client = mock.Mock()
    task = Task({"task_id": "t1"}, client)
    item = FeedbackItem.comment(Scope.scene(frames=0), "dark")

    task.create_fixless_audit(
        RESPONSE_URL, False, feedback_items=[item], comments="see items"
    )
    client.create_fixless_audit.assert_called_once_with(
        "t1", RESPONSE_URL, False, feedback_items=[item], comments="see items"
    )

    assert task.audits() is client.get_task_audits.return_value
    client.get_task_audits.assert_called_once_with("t1")


def test_api_treats_201_as_success():
    api = Api("test_dummy")
    created = mock.Mock(status_code=201)
    created.json.return_value = {"id": "audit_1"}
    with mock.patch.object(Api, "_http_request", return_value=created):
        assert api.put_request("audits", body={}) == {"id": "audit_1"}
