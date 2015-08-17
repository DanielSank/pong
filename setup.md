1. Set up basic environment. We assume virtualenvwrapper is set up on your system.
  1. `$ git clone .../pong.git`
  1. `$ cd pong` # We refer to this directory as PROJECT_ROOT
  1. `$ mkvirtualenv pong`
  1. `$ cd pong`
  1. `$ mkdir lib`
  1. `$ pip install -t ./lib sqlalchemy wtforms`
  1. `$ pip install alembic`
  1. `$ add2virtualenv PROJECT_ROOT/pong/lib`

1. Install mysql server: `$ sudo apt-get install mysql-server`.
We recommend not setting a root password on your local server as this simplifies your development work flow.
However, if you don't set password don't mysql server listen on open the internet.
To set up mysql server without a password, when asked for a root password during installation just leave it blank and hit enter.
The installer may ask several times.

1. Set up the local database
  1. `$ sudo mysql` and then in the mysql shell:
    1. `CREATE DATABASE pong;`
    1. `exit`
  1. `$ pip install mysql-python`
    1. Do NOT use `mysql-connector`.
    1. This step might fail on Windows. If it does, download a wheel and install that.
  1. Update database tables:
    1. `$ cd PROJECT_ROOT/pong`
    1. `$ alembic upgrade head`

  1. Set up the database url (includes setup for production database). Make a file `PROJECT_ROOT/pong/config.py` which looks like this:
    ```
    import util

    config = {}

    DB_NAME = <database name>
    USERNAME = <your name for database access>
    PASSWORD = <you database access password>
    DB_IP = <IP address of database>
    INSTANCE_ID = <cloud SQL instance name, e.g. "google.com:qh-pong:pong">

    if util.in_production_mode():
        config['DB_URL'] = "mysql+gaerdbms:///{}?instance={}".format(
            DB_NAME, INSTANCE_ID)
    else:
        config['DB_URL'] = "mysql://localhost/{}".format(DB_NAME)

    # External database access, uncomment for running migrations from local machine
    # config['DB_URL'] =r"mysql://{}:{}@{}/{}".format(USERNAME, PASSWORD, DB_IP, DB_NAME)
    ```
    There are three use cases here:
    1. Running in production mode.
    1. Running in local dev mode.
    1. Accessing the production database from your own computer.
You would do this, for example, when running migrations against the production database from your own computer.
This is the only case in which the username, password, and IP address are used.
When doing this uncomment the last line to set `DB_URL` appropriately, and also comment out the `import util` line.

1. Install the Google App Engine python SDK:
  1. Download it from the official site.
  1. Unpack it and put it somewhere like `~/src/` so that you have e.g. `~/src/google_appengine/`.

1. Run the server
  1. `$ cd PROJECT_ROOT`
  1. `$ python ~/path/to/google_appengine/dev_appserver.py .`. Note that you're running the dev server with your virtualenv's python interpreter.
  1. You can now use the pong application at `localhost:8080/users` and `localhost:8080/games/view`.

1. To make a new migration do `$ alembic revision --autogenerate -m "<message>"`

1. If starting from absolute scratch (i.e. you did not clone this github repo but are making your own project) you need to configure alembic
  1. `$ alembic init alembic`
  1. In `alembic.ini`, set a line to `sqlalchemy.url = 'bogus'`.
  1. In `alembic/env.py` add the following sections:

    ```
    # Get the full database url
    import projectname.config as myconfig
    config.set_main_option(
        'sqlalchemy.url',
        myconfig.config.get('DB_URL')
    )
    #<snip>
    # Add models' MetaData object for 'autogenerate' support.
    # We assume that pyle/projectname is in the system path
    import projectname.models as models
    target_metadata = models.Base.metadata
    ```
