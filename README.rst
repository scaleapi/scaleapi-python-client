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

Create categorization task
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

Create transcription task
=========================

Check `this`__ for further information.

__ https://scale.com/docs/#create-ocr-transcription-task

.. code-block:: python

    task = client.create_transcription_task(
      callback_url='http://www.example.com/callback',
      instruction='Transcribe the given fields. Then for each news item on the page, transcribe the information for the row.',
      attachment_type='website',
      attachment='http://www.google.com/',
      fields={ 'title': 'Title of Webpage', 'top_result': 'Title of the top result' },
      row_fields={ 'username': 'Username of submitter', 'comment_count': 'Number of comments' }
    )

Create comparison task
======================

Check `this`__ for further information.

__ https://scale.com/docs/#create-comparison-task

.. code-block:: python

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

Create annotation task
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

Create datacollection task
=========================

Check `this`__ for further information.

__ https://scale.com/docs/#create-data-collection-task

.. code-block:: python

    task = client.create_datacollection_task(
      callback_url='http://www.example.com/callback',
      instruction='Find the URL for the hiring page for the company with attached website.',
      attachment_type='website',
      attachment='http://www.google.com/',
      fields={ 'hiring_page': 'Hiring Page URL' },
    )

Create audiotranscription task
==============================

Check `this`__ for further information.

__ https://scale.com/docs/#create-audio-transcription-task

.. code-block:: python

    task = client.create_audiotranscription_task(
        callback_url='http://www.example.com/callback',
        attachment_type='audio',
        attachment='https://storage.googleapis.com/deepmind-media/pixie/knowing-what-to-say/second-list/speaker-3.wav',
        verbatim=False
    )

Retrieve task
=============

Check `this`__ for further information.

__ https://scale.com/docs/#retrieve-a-task

Retrieve a task given its id.

.. code-block :: python

    task = client.fetch_task('asdfasdfasdfasdfasdfasdf')
    task.id == 'asdfasdfasdfasdfasdfasdf' # true

Cancel task
===========

Check `this`__ for further information.

__ https://scale.com/docs/#cancel-a-task

Cancel a task given its id, only if it's not completed.

.. code-block :: python

    task = client.cancel_task('asdfasdfasdfasdfasdfasdf')

List tasks
==========

Check `this`__ for further information.

__ https://scale.com/docs/#list-all-tasks

Retrieve a list of tasks, with optional filter by date/type. Paginated with limit/offset.
The return value is a ``scaleapi.Tasklist``, which acts as a list, but also has fields
for the total number of tasks, the limit and offset, and whether or not there's more.

.. code-block :: python

    tasks = client.tasks(
        start_time='2015-10-13T22:38:42Z',
        end_time='2016-10-13T22:38:42Z',
        type='categorization',
        limit=100,
        offset=200)

    print(tasks.total)    # 1000
    print(tasks.limit)    # 100
    print(tasks.offset)   # 200
    print(tasks.has_more) # True

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

If you notice any problems, please email us at support@scaleapi.com.
