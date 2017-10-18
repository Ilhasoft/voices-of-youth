Voices of Youth
===============

This project is a new version of [UNICEF](www.unicef.org) initiative called [voices of youth](http://www.voicesofyouth.org/).

Running project
---------------

This project have a shell script that prepare the environment to execute the project.

Open the terminal and type:
```
./bootstrap.sh && source env/bin/activate
```

> This project requires python >= 3.6.

Default user
------------
The system automatically create the user **admin** with password **Un1c3f@@**.

Database
--------

We ship inside the docker directory, all files do you need to create a container with postgis database.

Type this command:
```
$(cd docker && docker-compose start)
```

Documentation
-------------
This project is shipped with documentation for developers and user. This section describe how to generate each of them.

We use [sphinx](http://www.sphinx-doc.org/en/stable/) to generate the documentation.

The sections bellow describe how to generate HTML versions of this documentations.

> After execute commands to generate the documentation, you just need to open the file **build/html/index.html** inside the respective documentation directory.

#### Development documentation

```
cd docs/dev && make html
```

### User

```
cd docs/user && make html
```

Test
----
We use [unittest](https://docs.python.org/3/library/unittest.html) to write project tests.

To the tests you have two options, with coverage and without coverage.

### With coverage

```
$ coverage run manage.py test && coverage report
```

### Without coverage

```
$ python manage.py test
```
