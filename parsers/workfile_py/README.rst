Workfile
===============
Workfile is an specification on how we can achieve the project management in a single plain text file format. 
Too many fields in a form to describe milestones, tasks, assignments, etc ? 
Workfile approach is to have one big text box

Installing
============

.. code-block:: bash

    pip install workfile

Usage
=====

.. code-block:: bash

    >>> import workfile
    >>> workfile.loads(text)
    >>> workfile.load(file_pointer)
