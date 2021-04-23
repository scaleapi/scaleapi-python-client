
# SDK Migration Guide to v2


If you are migrating from v0 or v1,  this guide explains how to update your application for compatibility with v2. We recommend migrating as soon as possible to ensure that your application is unaffected.

### Creating New Tasks

Methods with task types such as `create_imageannotation_task`, `create_textcollection_task` etc. are ~~**deprecated**~~.

Creating a new task is now unified under the `create_task(TaskType, ...)` method. Please review [Create Task](../README.rst#create-task) section for more details.


```python
# Deprecated Old Method
client.create_imageannotation_task(
    project = 'test_project',
    instruction= "Draw a box around each baby cow and big cow.",
    ...
)

# New Method
from scaleapi.tasks import TaskType

client.create_task(
    TaskType.ImageAnnotation,
    project = 'test_project',
    instruction= "Draw a box around each baby cow and big cow.",
    ...
)
```

### Retrieving Tasks

A new generator method is introduced to retrieve a list of tasks with all available parameters. The new method `get_tasks(...)` handles pagination and tokens.
You can have a simpler code by replacing `tasks()` loops with a single `get_tasks()` call.

Please refer to [List Tasks](../README.rst#list-tasks) for more details.

### Accessing Attributes (Task, Batch, Project)

The old `param_dict` attribute is now replaced with a method `as_dict()` to return an object's attributes as a dictionary.

First-level attributes of Task are still accessible with `.` annotation as the following:

```python
task.status                   # same as task.as_dict()["status"]
task.params["geometries"]     # same as task.as_dict()["params"]["geometries"]
task.response["annotations"]  # same as task.as_dict()["response"]["annotations"]
```

Accessing `task.params` child objects directly at task level is ~~**deprecated**~~. Instead of `task.attribute`, you should use `task.params["attribute"]` for accessing objects under `params`.

```python
task.params["geometries"]   # DEPRECATED access => task.geometries
task.params["attachment"]   # DEPRECATED access => task.attachment
```

### Task Counts as Summary of Batch

Attributes of Batch `pending`, `completed`, `error`, `canceled` are replaced with `tasks_pending`, `tasks_completed`, `tasks_error`, `tasks_canceled` respectively to avoid confusion.

```python
# NEW Attributes            # DEPRECATED Attributes

batch.tasks_pending         # batch.pending
batch.tasks_completed       # batch.completed
batch.tasks_error           # batch.error
batch.tasks_canceled        # batch.canceled
```

### Deprecated Methods

- `fetch_task()` replaced with `get_task()`
- `list_batches()`  replaced with `get_batches()`

### Enabled Auto-Retry

SDK now supports auto-retry in case of a `408`, `429` or `5xx` error occurs.

### New Exceptions

New error types are introduces if you want to handle specific exception cases.
`ScaleInvalidRequest`, `ScaleUnauthorized`, `ScaleNotEnabled`, `ScaleResourceNotFound`, `ScaleDuplicateTask`, `ScaleTooManyRequests`, `ScaleInternalError` and `ScaleTimeoutError`.

All new error types are child of the existing `ScaleException` which can be used to handle all cases.

Please review [Error handling](../README.rst#error-handling) section for more details.
