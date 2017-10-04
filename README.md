Running project
---------------

This project have a shell script that prepare the environment to execute the project.

Open the terminal and type:
```
./bootstrap.sh && source env/bin/activate
```

Database
--------

We ship inside the docker directory, all files do you need to create a container with postgis database.

Type this command:
```
$(cd docker && docker-compose start)
```
