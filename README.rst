Install
=======

These instructions assume that ``git``, ``docker``, and ``docker-compose`` are
installed on your host machine.

Local development
-----------------

First, clone this repo and make some required directories::

    $ git clone https://github.com/pyprogrammerblog/therapieland.git
    $ cd therapieland

Then build the docker image, providing your user and group ids for correct file
permissions::

    $ docker-compose build

Get inside app service::

    docker-compose run --rm app bash

Run migrations inside docker::

    (docker) $ python manage.py migrate

Then exit the docker shell (Ctrl + D)

At this point, you may want to test your installation::

    $ docker-compose run --rm app python manage.py test

Or start working with this app right away::

    $ docker-compose up
