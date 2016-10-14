import pytest
import scaleapi
import os

try:
    test_api_key = os.environ['SCALE_TEST_API_KEY']
    client = scaleapi.ScaleClient(test_api_key)
except KeyError:
    raise Exception("Please set the environment variable SCALE_TEST_API_KEY to run tests.")


def test_categorize_ok():
    task = client.create_categorization_task(
        callback_url='http://www.example.com/callback',
        instruction='Is this company public or private?',
        attachment_type='website',
        attachment='http://www.google.com/',
        categories=['public', 'private'])


def test_categorize_fail():
    with pytest.raises(scaleapi.ScaleInvalidRequest):
        client.create_categorization_task(
            callback_url='http://www.example.com/callback',
            categories=['public', 'private'])


def test_transcrption_ok():
    task = client.create_transcription_task(
        callback_url='http://www.example.com/callback',
        instruction='Transcribe the given fields. Then for each news item on the page, transcribe the information for the row.',
        attachment_type='website',
        attachment='http://www.google.com/',
        fields={
            'title': 'Title of Webpage',
            'top_result': 'Title of the top result'
        },
        row_fields={
            'username': 'Username of submitter',
            'comment_count': 'Number of comments'
        })


def test_transcription_fail():
    with pytest.raises(scaleapi.ScaleInvalidRequest):
        client.create_transcription_task(
            callback_url='http://www.example.com/callback',
            attachment_type='website')


def test_phonecall_ok():
    task = client.create_phonecall_task(
        callback_url='http://www.example.com/callback',
        instruction='Call this person and follow the script provided, recording responses',
        phone_number='5055006865',
        entity_name='Alexandr Wang',
        script='Hello ! Are you happy today? (pause) One more thing - what is your email address?',
        fields={'email': 'Email Address'},
        choices=['He is happy', 'He is not happy'])


def test_phonecall_fail():
    with pytest.raises(scaleapi.ScaleInvalidRequest):
        client.create_phonecall_task(
            callback_url='http://www.example.com/callback',
            instruction='Call this person and follow the script provided, recording responses')


def test_comparison_ok():
    task = client.create_comparison_task(
        callback_url='http://www.example.com/callback',
        instruction='Do the objects in these images have the same pattern?',
        attachment_type='image',
        attachments=[
            'http://i.ebayimg.com/00/$T2eC16dHJGwFFZKjy5ZjBRfNyMC4Ig~~_32.JPG',
            'http://images.wisegeek.com/checkered-tablecloth.jpg'
        ],
        choices=['yes', 'no'])


def test_comparison_fail():
    with pytest.raises(scaleapi.ScaleInvalidRequest):
        client.create_comparison_task(
            callback_url='http://www.example.com/callback',
            instruction='Do the objects in these images have the same pattern?',
            attachment_type='image')


def test_annotation_ok():
    task = client.create_annotation_task(
        callback_url='http://www.example.com/callback',
        instruction='Draw a box around each **baby cow** and **big cow**',
        attachment_type='image',
        attachment='http://i.imgur.com/v4cBreD.jpg',
        objects_to_annotate=['baby cow', 'big cow'],
        with_labels=True)


def test_annotation_fail():
    with pytest.raises(scaleapi.ScaleInvalidRequest):
        client.create_annotation_task(
            callback_url='http://www.example.com/callback',
            instruction='Draw a box around each **baby cow** and **big cow**',
            attachment_type='image')


def test_cancel():
    task = client.create_annotation_task(
        callback_url='http://www.example.com/callback',
        instruction='Draw a box around each **baby cow** and **big cow**',
        attachment_type='image',
        attachment='http://i.imgur.com/v4cBreD.jpg',
        objects_to_annotate=['baby cow', 'big cow'],
        with_labels=True)

    # raises a scaleexception, because test tasks complete instantly
    with pytest.raises(scaleapi.ScaleException):
        task.cancel()


def test_task_retrieval():
    task = client.create_annotation_task(
        callback_url='http://www.example.com/callback',
        instruction='Draw a box around each **baby cow** and **big cow**',
        attachment_type='image',
        attachment='http://i.imgur.com/v4cBreD.jpg',
        objects_to_annotate=['baby cow', 'big cow'],
        with_labels=True)

    task2 = client.fetch_task(task.id)
    assert task.status == 'pending'
    assert task2.status == 'completed'
    assert task2.id == task.id
    assert task2.callback_url == task.callback_url
    assert task2.instruction == task.instruction
    assert task2.attachment_type == task.attachment_type
    assert task2.attachment == task.attachment
    assert task2.objects_to_annotate == task.objects_to_annotate
    assert task2.with_labels == task.with_labels
    assert task2.metadata == task.metadata
    assert task2.type == task.type
    assert task2.created_at == task.created_at


def test_task_retrieval_fail():
    with pytest.raises(scaleapi.ScaleException):
        client.fetch_task('fake_id_qwertyuiop')


def test_tasks():
    tasks = []
    for i in range(3):
        tasks.append(client.create_annotation_task(
            callback_url='http://www.example.com/callback',
            instruction='Draw a box around each **baby cow** and **big cow**',
            attachment_type='image',
            attachment='http://i.imgur.com/v4cBreD.jpg',
            objects_to_annotate=['baby cow', 'big cow'],
            with_labels=True))
    task_ids = {task.id for task in tasks}
    for task in client.tasks(limit=3):
        assert task.id in task_ids


def test_tasks_invalid():
    with pytest.raises(scaleapi.ScaleException):
        client.tasks(bogus=0)
