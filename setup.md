1. Set up basic environment. We assume virtualenvwrapper is set up on your system.
  1. `$ git clone .../pong.git`
  1. `$ cd pong` # We refer to this directory as PROJECT_ROOT
  1. `$ mkvirtualenv pong`
  1. `$ cd pong`
  1. `$ mkdir lib`
  1. `$ pip install -t ./lib sqlalchemy wtforms`
  1. `$ pip install alembic`
  1. `$ add2virtualenv ~/src/pong/pong/lib`

1. Install mysql server: `$ sudo apt-get install mysql-server`. When asked for a root password leave it blank and hit enter. You might need to do this more than once.

1. Set up the database
  1. `$ sudo mysql` and then in the mysql shell:
    1. `CREATE DATABASE pong;`
    1. `exit`
  1. `$ pip install mysql-python`
    1. Do NOT use `mysql-connector`.
    1. This step might fail on Windows. If it does, download a wheel and install that.
  1. Update database tables: `$ alembic upgrade head` (needs project on python system path)

  1. Set up the database url: make a file `PROJECT_ROOT/pong/config.py` which looks like this:

    ```
    config = {
        'DB_URL': <database url>
    } 
    ```

1. Install the Google App Engine python SDK:
  1. Download it from the official site.
  1. Unpack it and put it somewhere like `~/src/` so that you have e.g. `~/src/google_appengine/`.

1. Run the server
  1. `$ cd PROJECT_ROOT`
  1. `$ python ~/src/google_appengine/dev_appserver.py .`. Note that you're running the dev server with your virtualenv's python interpreter.
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
