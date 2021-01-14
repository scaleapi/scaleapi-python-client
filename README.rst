===================
ScaleAPI for Python
===================


Installation
============
.. code-block:: bash

    $ pip install --upgrade scaleapi
    
Note: We strongly suggest using `scaleapi` with Python version 2.7.9 or greater due to SSL issues with prior versions.

Usage
=====
.. code-block:: python

    import scaleapi
    client = scaleapi.ScaleClient('YOUR_API_KEY_HERE')

Tasks
=====

Most of these methods will return a ``scaleapi.Task`` object, which will contain information
about the json response (task_id, status...).

Any parameter available in the documentation_ can be passed as an argument option with the corresponding type.

.. _documentation: https://scale.com/docs

The following endpoints for tasks are available:

Create Categorization Task
==========================

Check `this`__ for further information.

__ https://scale.com/docs/#create-categorization-task

.. code-block:: python

    task = client.create_categorization_task(
      callback_url='http://www.example.com/callback',
      instruction='Is this company public or private?',
      attachment_type='website',
      attachment='http://www.google.com/',
      categories=['public', 'private']
    )

Create Annotation Task
======================

Check `this`__ for further information.

__ https://scale.com/docs/#2d-box-annotation

.. code-block:: python

    client.create_annotation_task(
      callback_url='http://www.example.com/callback',
      instruction='Draw a box around each baby cow and big cow.',
      attachment_type="image",
      attachment="http://i.imgur.com/v4cBreD.jpg",
      objects_to_annotate=["baby cow", "big cow"]
    )

Retrieve task
=============

Check `this`__ for further information.

__ https://docs.scale.com/reference#retrieve-tasks

Retrieve a task given its id.

.. code-block :: python

    task = client.fetch_task('asdfasdfasdfasdfasdfasdf')
    task.id == 'asdfasdfasdfasdfasdfasdf' # true

Cancel task
===========

Check `this`__ for further information.

__ https://docs.scale.com/reference#cancel-task

Cancel a task given its id, only if it's not completed.

.. code-block :: python

    task = client.cancel_task('asdfasdfasdfasdfasdfasdf')

List tasks
==========

Check `this`__ for further information.

__ https://docs.scale.com/reference#list-multiple-tasks

Retrieve a list of tasks, with optional filter by date/type. Paginated with limit/offset.
The return value is a ``scaleapi.Tasklist``, which acts as a list, but also has fields
for the total number of tasks, the limit and offset, and whether or not there's more.

.. code-block :: python

    next_token = None;
    counter = 0
    all_tasks =[]
    while True:
        tasks = client.tasks(
            start_time = "2020-09-08",
            end_time = "2021-01-01",
            customer_review_status = "accepted",
            next_token = next_token,
        )
        for task in tasks:
            counter += 1
            print(f'Downloading Task {counter} | {task.task_id}')
            all_tasks.append(task.__dict__['param_dict'])
        next_token = tasks.next_token
        if next_token is None:
            break
    print(all_tasks)

Error handling
==============

If something went wrong while making API calls, then exceptions will be raised automatically
as a ``scaleapi.ScaleException``  or ``scaleapi.ScaleInvalidRequest`` runtime error. For example:

.. code-block:: python

    try
        client.create_categorization_task('Some parameters are missing.')
    except scaleapi.ValidationError as e:
        print(e.code)  # 400
        print(e.message)  # missing param X

Troubleshooting
===============

If you notice any problems, please email us at support@scale.com.
