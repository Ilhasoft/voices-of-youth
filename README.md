Running project
---------------

This project have a shell script that prepare the environment to execute the project.

Open the terminal and type:
```
./bootstrap.sh && source env/bin/activate
```

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
