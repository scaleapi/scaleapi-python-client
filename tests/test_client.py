# coding: utf-8

import pytest
import scaleapi
import time
from datetime import datetime
import os

try:
    test_api_key = os.environ['SCALE_TEST_API_KEY']
    client = scaleapi.ScaleClient(test_api_key)
except KeyError:
    raise Exception("Please set the environment variable SCALE_TEST_API_KEY to run tests.")

def make_a_task():
    return client.create_task(
        task_type = 'imageannotation',
        callback_url = "http://www.example.com/callback",
        instruction = "Draw a box around each baby cow and big cow.",
        attachment_type = "image",
        attachment = "http://i.imgur.com/v4cBreD.jpg",
        geometries = {
            "box": {
              "objects_to_annotate": ["Baby Cow", "Big Cow"],
              "min_height": 10,
              "min_width": 10
            }
        }
    )

def test_categorize_ok():
    task = client.create_task(
        task_type = 'categorization',
        callback_url='http://www.example.com/callback',
        instruction='Is this company public or private?',
        attachment_type='website',
        attachment='http://www.google.com/',
        categories=['public', 'private'])

def test_categorize_fail():
    with pytest.raises(scaleapi.ScaleInvalidRequest):
        client.create_task(
            task_type = 'categorization',
            callback_url='http://www.example.com/callback',
            categories=['public', 'private'])

def test_transcription_ok():
    task = client.create_task(
        task_type = 'categorization',
        callback_url='http://www.example.com/callback',
        instruction='Transcribe the given fields. Then for each news item on the page, transcribe the information for the row.',
        attachment_type='website',
        attachment='http://www.google.com/',
        fields={
            'title': 'Title of Webpage',
            'top_result': 'Title of the top result'
        },
        repeatable_fields={
            'username': 'Username of submitter',
            'comment_count': 'Number of comments'
        })

def test_transcription_fail():
    with pytest.raises(scaleapi.ScaleInvalidRequest):
        client.create_task(
            task_type='transcription',
            callback_url='http://www.example.com/callback',
            attachment_type='website')

def test_imageannotation_ok():
    client.create_task(
        task_type = 'imageannotation',
        callback_url = "http://www.example.com/callback",
        instruction = "Draw a box around each baby cow and big cow.",
        attachment_type = "image",
        attachment = "http://i.imgur.com/v4cBreD.jpg",
        geometries = {
            "box": {
              "objects_to_annotate": ["Baby Cow", "Big Cow"],
              "min_height": 10,
              "min_width": 10
            }
        }
    )
    # min_width and min_height should be optional
    task2 = client.create_task(
        task_type = 'imageannotation',
        callback_url='http://www.example.com/callback',
        instruction='Draw a box around each **baby cow** and **big cow**',
        attachment_type='image',
        attachment='http://i.imgur.com/v4cBreD.jpg',
        geometries = {
            "box": {
              "objects_to_annotate": ["Baby Cow", "Big Cow"],
              "min_height": 10,
              "min_width": 10
            }
        })

def test_imageannotation_fail():
    with pytest.raises(scaleapi.ScaleInvalidRequest):
        client.create_task(
            task_type = 'imageannotation',
            callback_url='http://www.example.com/callback',
            instruction='Draw a box around each **baby cow** and **big cow**',
            attachment_type='image')

def test_cancel():
    task = make_a_task()
    # raises a scaleexception, because test tasks complete instantly
    with pytest.raises(scaleapi.ScaleException):
        task.cancel()

def test_task_retrieval():
    task = make_a_task()
    task2 = client.fetch_task(task.id)
    assert task.status == 'pending'
    assert task2.status == 'completed'
    assert task2.id == task.id
    assert task2.callback_url == task.callback_url
    assert task2.instruction == task.instruction
    assert task2.attachment_type == task.attachment_type
    assert task2.attachments == task.attachments
    assert task2.choices == task.choices
    assert task2.metadata == task.metadata
    assert task2.type == task.type
    assert task2.created_at == task.created_at

def test_task_retrieval_time():
    task = make_a_task()
    time.sleep(0.5)
    start_time = datetime.utcnow().isoformat()
    time.sleep(0.5)
    end_time = datetime.utcnow().isoformat()
    tasks = client.tasks(start_time=start_time, end_time=end_time)
    assert tasks.docs == []

def test_task_retrieval_fail():
    with pytest.raises(scaleapi.ScaleException):
        client.fetch_task('fake_id_qwertyuiop')

def test_tasks():
    tasks = []
    for i in range(3):
        tasks.append(make_a_task())
    task_ids = {task.id for task in tasks}
    for task in client.tasks(limit=3):
        assert task.id in task_ids

def test_tasks_invalid():
    with pytest.raises(scaleapi.ScaleException):
        client.tasks(bogus=0)

def create_a_batch():
    return client.create_batch(
        callback = "http://www.example.com/callback",
        batch_name = "kitten_labeling_2020-07",
        project = "kitten_labeling"
    )

def test_finalize_batch():
    batch = create_a_batch()
    client.finalize_batch(batch.name)

def get_batch_status():
    batch = create_a_batch()
    client.batch_status(batch.name)

def get_batch():
    batch = create_a_batch()
    client.get_batch(batch.name)

def 