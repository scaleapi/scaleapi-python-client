# pylint: disable=missing-function-docstring
import os
import time
import uuid
from datetime import datetime

import pytest

import scaleapi
from scaleapi.batches import BatchStatus
from scaleapi.exceptions import (
    ScaleDuplicateResource,
    ScaleInvalidRequest,
    ScaleResourceNotFound,
    ScaleUnauthorized,
)
from scaleapi.tasks import TaskType

# from scaleapi.teams import TeammateRole

TEST_PROJECT_NAME = "scaleapi-python-sdk"

try:
    print(f"SDK Version: {scaleapi.__version__}")
    test_api_key = os.environ["SCALE_TEST_API_KEY"]

    if test_api_key.startswith("test_") or test_api_key.endswith("|test"):
        client = scaleapi.ScaleClient(test_api_key, "pytest")
    else:
        raise Exception("Please provide a valid TEST environment key.")
except KeyError as err:
    raise Exception(
        "Please set the environment variable SCALE_TEST_API_KEY to run tests."
    ) from err

try:
    project = client.get_project(TEST_PROJECT_NAME)
except ScaleResourceNotFound:
    client.create_project(
        project_name=TEST_PROJECT_NAME, task_type=TaskType.ImageAnnotation
    )


def test_invalidkey_fail():
    client_fail = scaleapi.ScaleClient("dummy_api_key", "pytest")
    with pytest.raises(ScaleUnauthorized):
        client_fail.batches(limit=1)


def make_a_task(unique_id: str = None, batch: str = None):
    args = {
        "callback_url": "http://www.example.com/callback",
        "instruction": "Draw a box around each baby cow and big cow.",
        "attachment_type": "image",
        "attachment": "http://i.imgur.com/v4cBreD.jpg",
        "geometries": {
            "box": {
                "objects_to_annotate": ["Baby Cow", "Big Cow"],
                "min_height": 10,
                "min_width": 10,
            }
        },
    }
    if unique_id:
        args["unique_id"] = unique_id
    if batch:
        args["batch"] = batch

    return client.create_task(TaskType.ImageAnnotation, **args)


def test_unique_id_fail():
    unique_id = str(uuid.uuid4())
    make_a_task(unique_id)
    with pytest.raises(ScaleDuplicateResource):
        make_a_task(unique_id)


def test_update_unique_id():
    unique_id = str(uuid.uuid4())
    task = make_a_task(unique_id)
    unique_id_new = str(uuid.uuid4())

    task = client.update_task_unique_id(task.id, unique_id_new)
    assert unique_id_new == task.as_dict()["unique_id"]


def test_clear_unique_id():
    unique_id = str(uuid.uuid4())
    task = make_a_task(unique_id)

    task = client.clear_task_unique_id(task.id)
    assert "unique_id" not in task.as_dict()


def test_set_metadata():
    unique_id = str(uuid.uuid4())
    original_task = make_a_task(unique_id)
    new_metadata = {"myKey": "myValue"}
    updated_task = client.set_task_metadata(original_task.id, new_metadata)
    assert original_task.metadata == {}
    assert updated_task.metadata == new_metadata


def test_task_set_metadata():
    unique_id = str(uuid.uuid4())
    task = make_a_task(unique_id)
    assert task.metadata == {}
    new_metadata = {"fromTaskKey": "fromTaskValue"}
    task.set_metadata(new_metadata)
    task.refresh()
    assert task.metadata == new_metadata


def test_set_task_tags():
    unique_id = str(uuid.uuid4())
    task = make_a_task(unique_id)
    assert not hasattr(task, "tags")
    new_tags = ["tag1", "tag2", "tag3"]
    task.set_tags(new_tags)
    task.refresh()
    assert task.tags == new_tags


def test_add_task_tags():
    unique_id = str(uuid.uuid4())
    task = make_a_task(unique_id)
    assert not hasattr(task, "tags")
    new_tags = ["tag1", "tag2", "tag3"]
    task.add_tags(new_tags)
    task.refresh()
    assert task.tags == new_tags


def test_delete_task_tags():
    unique_id = str(uuid.uuid4())
    task = make_a_task(unique_id)
    assert not hasattr(task, "tags")
    new_tags = ["tag1", "tag2", "tag3"]
    task.add_tags(new_tags)
    task.delete_tags(["tag1", "tag2"])
    task.refresh()
    assert task.tags == ["tag3"]


def test_categorize_ok():
    client.create_task(
        TaskType.Categorization,
        callback_url="http://www.example.com/callback",
        instruction="Is this company public or private?",
        attachment_type="website",
        force=True,
        attachment="http://www.google.com/",
        categories=["public", "private"],
    )


def test_categorize_fail():
    with pytest.raises(ScaleInvalidRequest):
        client.create_task(
            TaskType.Categorization,
            callback_url="http://www.example.com/callback",
            categories=["public", "private"],
        )


def test_transcription_ok():
    client.create_task(
        TaskType.Transcription,
        callback_url="http://www.example.com/callback",
        instruction="Transcribe the given fields. "
        "Then for each news item on the page, "
        "transcribe the information for the row.",
        attachment_type="website",
        attachment="http://www.google.com/",
        fields={
            "title": "Title of Webpage",
            "top_result": "Title of the top result",
        },
        repeatable_fields={
            "username": "Username of submitter",
            "comment_count": "Number of comments",
        },
    )


def test_transcription_fail():
    with pytest.raises(ScaleInvalidRequest):
        client.create_task(
            TaskType.Transcription,
            callback_url="http://www.example.com/callback",
            attachment_type="website",
        )


def test_imageannotation_ok():
    client.create_task(
        TaskType.ImageAnnotation,
        callback_url="http://www.example.com/callback",
        instruction="Draw a box around each baby cow and big cow.",
        attachment_type="image",
        attachment="http://i.imgur.com/v4cBreD.jpg",
        geometries={
            "box": {
                "objects_to_annotate": ["Baby Cow", "Big Cow"],
                "min_height": 10,
                "min_width": 10,
            }
        },
    )


def test_imageannotation_fail():
    with pytest.raises(ScaleInvalidRequest):
        client.create_task(
            TaskType.ImageAnnotation,
            callback_url="http://www.example.com/callback",
            instruction="Draw a box around each **baby cow** and **big cow**",
            attachment_type="image",
        )


def test_documenttranscription_ok():
    client.create_task(
        TaskType.DocumentTranscription,
        instruction="Please transcribe this receipt.",
        attachment="http://document.scale.com/receipt-20200519.jpg",
        features=[{"type": "block", "label": "barcode"}],
    )


def test_documenttranscription_fail():
    with pytest.raises(ScaleInvalidRequest):
        client.create_task(
            TaskType.DocumentTranscription,
            callback_url="http://www.example.com/callback",
            instruction="Please transcribe this receipt.",
        )


def test_annotation_ok():
    client.create_task(
        TaskType.Annotation,
        callback_url="http://www.example.com/callback",
        instruction="Draw a box around each **baby cow** and **big cow**",
        attachment_type="image",
        attachment="http://i.imgur.com/v4cBreD.jpg",
        min_width="30",
        min_height="30",
        objects_to_annotate=["baby cow", "big cow"],
        with_labels=True,
    )


def test_annotation_fail():
    with pytest.raises(ScaleInvalidRequest):
        client.create_task(
            TaskType.Annotation,
            callback_url="http://www.example.com/callback",
            instruction="Draw a box around each **baby cow** and **big cow**",
            attachment_type="image",
        )


def test_polygonannotation_ok():
    client.create_task(
        TaskType.PolygonAnnotation,
        callback_url="http://www.example.com/callback",
        instruction="Draw a tight shape around the big cow",
        attachment_type="image",
        attachment="http://i.imgur.com/v4cBreD.jpg",
        objects_to_annotate=["big cow"],
        with_labels=True,
    )


def test_polygonannotation_fail():
    with pytest.raises(ScaleInvalidRequest):
        client.create_task(
            TaskType.PolygonAnnotation,
            callback_url="http://www.example.com/callback",
            instruction="Draw a tight shape around the big cow",
            attachment_type="image",
        )


def test_lineannotation_ok():
    client.create_task(
        TaskType.LineAnnotation,
        callback_url="http://www.example.com/callback",
        instruction="Draw a tight shape around the big cow",
        attachment_type="image",
        attachment="http://i.imgur.com/v4cBreD.jpg",
        objects_to_annotate=["big cow"],
        with_labels=True,
    )


def test_lineannotation_fail():
    with pytest.raises(ScaleInvalidRequest):
        client.create_task(
            TaskType.LineAnnotation,
            callback_url="http://www.example.com/callback",
            instruction="Draw a tight shape around the big cow",
            attachment_type="image",
        )


def test_datacollection_ok():
    client.create_task(
        TaskType.DataCollection,
        callback_url="http://www.example.com/callback",
        instruction="Find the URL for the hiring page for the company"
        " with attached website.",
        attachment_type="website",
        attachment="http://www.google.com/",
        fields={"hiring_page": "Hiring Page URL"},
    )


def test_datacollection_fail():
    with pytest.raises(ScaleInvalidRequest):
        client.create_task(
            TaskType.DataCollection,
            callback_url="http://www.example.com/callback",
            attachment_type="website",
        )


def test_namedentityrecognition_ok():
    return client.create_task(
        TaskType.NamedEntityRecognition,
        callback_url="http://www.example.com/callback",
        instruction="Do the objects in these images have the same pattern?",
        text="Example text to label with NER tool",
        labels=[{"name": "Label_A", "description": "the first label"}],
    )


def test_cancel():
    task = make_a_task()
    # raises a scaleexception, because test tasks complete instantly
    with pytest.raises(ScaleInvalidRequest):
        task.cancel()


def test_task_retrieval():
    task = make_a_task()
    task2 = client.get_task(task.id)
    assert task2.status == "completed"
    assert task2.id == task.id
    assert task2.callback_url == task.callback_url
    assert task2.instruction == task.instruction
    assert task2.params["attachment_type"] == task.params["attachment_type"]
    assert task2.params["attachment"] == task.params["attachment"]
    assert task2.params["geometries"] == task.params["geometries"]
    assert task2.metadata == task.metadata
    assert task2.type == task.type
    assert task2.created_at == task.created_at


def test_task_retrieval_time():
    make_a_task()
    time.sleep(0.5)
    start_time = datetime.utcnow().isoformat()
    time.sleep(0.5)
    end_time = datetime.utcnow().isoformat()
    tasks = client.tasks(start_time=start_time, end_time=end_time)
    assert tasks.docs == []


def test_task_retrieval_fail():
    with pytest.raises(ScaleResourceNotFound):
        client.get_task("fake_id_qwertyuiop")


def test_tasks():
    tasks = []
    for _ in range(3):
        tasks.append(make_a_task())
    task_ids = {task.id for task in tasks}
    for task in client.tasks(limit=3):
        assert task.id in task_ids


def test_tasks_invalid():
    with pytest.raises(ScaleInvalidRequest):
        client.tasks(bogus=0)


def create_a_batch():
    return client.create_batch(
        callback="http://www.example.com/callback",
        batch_name=str(uuid.uuid4()),
        project=TEST_PROJECT_NAME,
        metadata={"some_key": "some_value"},
    )


def test_get_tasks():
    batch = create_a_batch()
    tasks = []
    for _ in range(3):
        tasks.append(make_a_task(batch=batch.name))
    task_ids = {task.id for task in tasks}
    for task in client.get_tasks(
        project_name=TEST_PROJECT_NAME,
        batch_name=batch.name,
        limit=1,
    ):
        assert task.id in task_ids


def test_get_tasks_count():
    tasks_count = client.tasks(project=TEST_PROJECT_NAME).total
    get_tasks_count = client.get_tasks_count(project_name=TEST_PROJECT_NAME)
    assert tasks_count == get_tasks_count


def test_get_tasks_count_with_only_batch():
    batch = create_a_batch()
    tasks_count = client.tasks(batch=batch.name).total
    get_tasks_count = client.get_tasks_count(batch_name=batch.name)
    assert tasks_count == get_tasks_count


def test_finalize_batch():
    batch = create_a_batch()
    batch = client.finalize_batch(batch.name)

    batch2 = create_a_batch()
    batch2.finalize()


def test_get_batch_status():
    batch = create_a_batch()
    client.batch_status(batch.name)
    assert batch.status == BatchStatus.InProgress.value

    batch2 = client.get_batch(batch.name)
    batch2.get_status()  # Test status update
    assert batch2.status == BatchStatus.InProgress.value


def test_get_batch():
    batch = create_a_batch()
    batch2 = client.get_batch(batch.name)
    assert batch.name == batch2.name
    assert batch2.status == BatchStatus.InProgress.value
    # test metadata
    assert batch2.metadata["some_key"] == "some_value"


def test_batches():
    batches = []
    for _ in range(3):
        batches.append(create_a_batch())
    batch_names = {batch.name for batch in batches}

    for batch in client.batches(limit=3):
        assert batch.name in batch_names


def test_get_batches():
    # Get count of all batches
    batchlist = client.batches(project=TEST_PROJECT_NAME, limit=1)
    total_batches = batchlist.total

    # Download all batches to check total count
    all_batches = list(client.get_batches(project_name=TEST_PROJECT_NAME))
    assert total_batches == len(all_batches)


def test_set_batch_metadata():
    batch = create_a_batch()
    batch = client.set_batch_metadata(batch.name, {"new_key": "new_value"})
    assert batch.metadata["new_key"] == "new_value"


def test_files_upload():
    with open("tests/test_image.png", "rb") as f:
        client.upload_file(
            file=f,
            project_name=TEST_PROJECT_NAME,
        )


def test_files_import():
    client.import_file(
        file_url="https://static.scale.com/uploads/selfserve-sample-image.png",
        project_name=TEST_PROJECT_NAME,
    )


# current_timestamp = str(uuid.uuid4)[-9:]
# TEST_USER = f"test+{current_timestamp}@scale.com"


def test_list_teammates():
    teammates = client.list_teammates()
    assert len(teammates) > 0


# def test_invite_teammates():
#     old_teammates = client.list_teammates()
#     new_teammates = client.invite_teammates(
#         [TEST_USER],
#         TeammateRole.Member,
#     )
#     assert len(new_teammates) >= len(
#         old_teammates
#     )  # needs to sleep for teammates list to be updated


def test_get_tasks_without_project_name():
    with pytest.raises(ValueError):
        list(client.get_tasks())


def test_get_tasks_with_optional_project_name():
    batch = create_a_batch()
    tasks = []
    for _ in range(3):
        tasks.append(make_a_task(batch=batch.name))
    task_ids = {task.id for task in tasks}
    for task in client.get_tasks(
        project_name=None,
        batch_name=batch.name,
        limit=1,
    ):
        assert task.id in task_ids


def test_process_tasks_endpoint_args_with_optional_project_name():
    args = client._process_tasks_endpoint_args(batch_name="test_batch")
    assert args["project"] is None
    assert args["batch"] == "test_batch"


def test_get_tasks_with_batch_name():
    batch = create_a_batch()
    tasks = []
    for _ in range(3):
        tasks.append(make_a_task(batch=batch.name))
    task_ids = {task.id for task in tasks}
    for task in client.get_tasks(
        batch_name=batch.name,
        limit=1,
    ):
        assert task.id in task_ids
