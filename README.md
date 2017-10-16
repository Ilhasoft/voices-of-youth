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
The documentation is generated use sphinx, and is splited in 2 areas, development and user.

The sections bellow describe how to generate HTML version of documentation.

### Development
To generate developer's documentation execute the commands bellow:

```
cd docs/dev && make html
```

This will generate all documentation inside the directory **docs/dev/build/html** just open the file **index.html** inside this directory.

### User
To generate user's documentation execute the commands bellow:

```
cd docs/user && make html
```

This will generate all documentation inside the directory **docs/user/build/html** just open the file **index.html** inside this directory.
