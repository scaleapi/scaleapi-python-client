# ScaleAPI for Python

## Installation
```sh
pip install scaleapi
```

## Usage
```python
import scale
client = scale.ScaleClient('YOUR_API_KEY_HERE', callback_key='OPTIONAL_CALLBACK_KEY_HERE')
```

### Tasks

Most of these methods will return a `scale.Task` object, which will contain information
about the json response (task_id, status...).

Any parameter available in the [documentation](https://docs.scaleapi.com) can be passed as an argument
option with the corresponding type.

The following endpoints for tasks are available:

#### Create categorization task

Check [this](https://docs.scaleapi.com/#create-categorization-task) for further information.

```python
task = client.create_categorization_task(
  callback_url='http://www.example.com/callback',
  instruction='Is this company public or private?',
  attachment_type='website',
  attachment='http://www.google.com/',
  categories=['public', 'private']
)
```

#### Create transcription task

Check [this](https://docs.scaleapi.com/#create-transcription-task) for further information.

```python
task = client.create_transcription_task(
  callback_url='http://www.example.com/callback',
  instruction='Transcribe the given fields. Then for each news item on the page, transcribe the information for the row.',
  attachment_type='website',
  attachment='http://www.google.com/',
  fields={ 'title': 'Title of Webpage', 'top_result': 'Title of the top result' },
  row_fields: { 'username': 'Username of submitter', 'comment_count': 'Number of comments' }
)
```

#### Create phone call task

Check [this](https://docs.scaleapi.com/#create-phone-call-task) for further information.

```python
client.create_phonecall_task(
  callback_url='http://www.example.com/callback',
  instruction="Call this person and tell me his email address. Ask if he's happy too.",
  phone_number='5055006865',
  entity_name='Alexandr Wang',
  fields={ 'email': 'Email Address' },
  choices=['He is happy', 'He is not happy']
)
```

#### Create comparison task

Check [this](https://docs.scaleapi.com/#create-comparison-task) for further information.

```python
client.create_comparison_task(
  callback_url='http://www.example.com/callback',
  instruction='Do the objects in these images have the same pattern?',
  attachment_type='image',
  choices=['yes', 'no'],
  attachments=[
    'http://i.ebayimg.com/00/$T2eC16dHJGwFFZKjy5ZjBRfNyMC4Ig~~_32.JPG',
    'http://images.wisegeek.com/checkered-tablecloth.jpg'
  ]
)
```

#### Create annotation task

Check [this](https://docs.scaleapi.com/#create-annotation-task-bounding-box) for further information.

```python
client.create_annotation_task(
  callback_url='http://www.example.com/callback',
  instruction='Draw a box around each baby cow and big cow.',
  attachment_type="image",
  attachment="http://i.imgur.com/v4cBreD.jpg",
  objects_to_annotate=["baby cow", "big cow"]
)
```

#### Retrieve task

Check [this](https://docs.scaleapi.com/#retrieve-a-task) for further information.

Retrieve a task given its id.

```python
task = client.retrieve_task('asdfasdfasdfasdfasdfasdf')
task.id == 'asdfasdfasdfasdfasdfasdf' # true
```

#### Cancel task

Check [this](https://docs.scaleapi.com/#cancel-a-task) for further information.

Cancel a task given its id, only if it's not completed.

```python
task = client.cancel_task('asdfasdfasdfasdfasdfasdf')
```

#### List tasks

Check [this](https://docs.scaleapi.com/#list-all-tasks) for further information.

Retrieve a list of all tasks.

```python
tasks = client.tasks()
```

## Error handling

If something went wrong while making API calls, then exceptions will be raised automatically
as a `scale.ScaleError`  or `scale.ValidationError` runtime error. For example:

```python
try
  scale.create_categorization_task('Some parameters are missing.')
except scale.ValidationError as e:
  print(e.code)  # 400
  print(e.message)  # missing param X
```

## Custom options

The api initialization accepts the following options:

| Name | Description | Default |
| ---- | ----------- | ------- |
| `endpoint` | Endpoint used in the http requests. | `'https://api.scaleapi.com/v1/'` |
| `api_key` | API key used in the http requests. | required |

