Derex User retire
=================


.. image:: https://dev.azure.com/abstract-technology/derex.userretire/_apis/build/status/Abstract-Tech.derex.userretire?branchName=master
    :target: https://dev.azure.com/abstract-technology/derex.userretire/_build


Derex Plugin to allow user retirement on Open edX.


Setup
-----

* Install this package with pip

.. code-block:: bash

    pip install "git+https://github.com/Abstract-Tech/derex.userretire.git#egg=derex.userretire"

* Add to the project derex.config.yaml

.. code-block:: yaml

    plugins:
      derex.userretire: {}

Development
-----------

* Install direnv_
* Allow direnv to create the virtualenv ::

    direnv allow

* Install with pip ::

    pip install -r requirements/requirements_dev.txt
    pre-commit install --install-hooks
