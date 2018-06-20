# Voices of Youth

This project is a new version of [UNICEF](www.unicef.org) initiative called [voices of youth](http://www.voicesofyouth.org/).

## Development database

The commands bellow starts 2 containers, one for database and other for pgadmin4. The database container port 5432 is binded to your host port 5432, and the pgadmin port 80 is binded to your host port 9000.

```bash
cd docker && docker-compose up voy_database pgadmin -d
```

Authentication data for pgadmin:

**Username:** dba@unicef.com
**Password:** SuperSecret

When you will add a new connection on pgadmin, the server address are:

```bash
server-address: voy-database
username: postgres
password: development
database: voydev
```

## Running project

### Configure the project

This project was built to follow the [12factor app](https://12factor.net/) because of that, all configurations can be maded using environment variables.
Here is the list of the variables that you can use to change some parts and behaviours of the voy:

| variable               | default value                                                            | example value                     | description                                                                                                |
|------------------------|--------------------------------------------------------------------------|-----------------------------------|------------------------------------------------------------------------------------------------------------|
| DEBUG                  | False                                                                    | True                              | Enable debug mode. Never use on production environment.                                                    |
| SECRET_KEY             | a random string                                                          | any random string > 40 characters | Used to provide cryptographic signing                                                                      |
| DATABASE_URL           | postgis://postgres:development@localhost:5432/voydev                     |                                   | URL for database server.                                                                                   |
| DEBUG_TOOLBAR          | False                                                                    | True                              |                                                                                                            |
| ALLOWED_HOSTS          | ['127.0.0.1', 'localhost']                                               | voicesofyouth.org                 | Used to indicate the host/domain that application can serve.                                               |
| CORS_ORIGIN_WHITELIST  | ('localhost:8000', '127.0.0.1:8000', 'localhost:8080', '127.0.0.1:8080') | voicesofyouth.org                 | Cross Origin Resource Sharing(CORS) is a W3C spec that allows cross domain communication from the browser. |
| CORS_ALLOW_CREDENTIALS | True                                                                     | False                             | If True, cookies will be allowed to be included in cross-site HTTP requests.                               |
| CORS_ORIGIN_ALLOW_ALL  | False                                                                    | True                              | If True, the whitelist will not be used and all origins will be accepted.                                  |
| EMAIL_HOST             |                                                                          | my.mail.server.com                | Email server FQDN.                                                                                         |
| EMAIL_PORT             | 465                                                                      | 465                               | Port used by server to stablish connections.                                                               |
| EMAIL_USE_SSL          | True                                                                     |                                   | Define whether the communication should be encrypted.                                                      |
| EMAIL_FROM             |                                                                          | foo@mail.server.com               | Email used in email from field.                                                                            |
| EMAIL_HOST_USER        |                                                                          | foo@mail.server.com               | User used on authenticate server procedures.                                                               |
| EMAIL_HOST_PASSWORD    |                                                                          | MyP4ssw0rd                        | Password used on autheticate server procedures.                                                            |

You can configure the variables in two ways:

### Running the project

To run this project just open the terminal and type:

```bash
pipenv install && pipenv shell
python manage.py migrate
python manage.py runserver

# Create admin user
python manage.py createsuperuser
```

> This project requires python >= 3.6.

## Documentation

This project is shipped with documentation for developers and user. This section describe how to generate each of them.

We use [sphinx](http://www.sphinx-doc.org/en/stable/) to generate the documentation.

The sections bellow describe how to generate HTML versions of this documentations.

> After execute commands to generate the documentation, you just need to open the file **build/html/index.html** inside the respective documentation directory.

### Development documentation

```bash
cd docs/dev && make html
```

### User

```bash
cd docs/user && make html
```

## Running tests

### With coverage

```bash
coverage run manage.py test && coverage report
```

### Without coverage

```bash
python manage.py test
```
