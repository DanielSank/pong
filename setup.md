1. Set up basic environment.
  1. `$ git clone .../pong.git`
  1. `$ cd pong` # We refer to this directory as PROJECT_ROOT
  1. `$ virtualenv env`
  1. `$ source ./env/bin/activate`
  1. `$ pip install sqlalchemy alembic wtforms`

1. Install mysql server: `$ sudo apt-get install mysql-server`. When asked for a root password leave it blank and hit enter. You might need to do this more than once.

1. Make a lib directory in the project root and symlink it to the virtualenv's site-packages.
  1. `$ cd PROJECT_ROOT/pong`
  1. `$ mkdir lib`
  1. `$ ln -s PROJECT_ROOT/env/lib/local/python2.7/site-packages lib`

1. Set up the database
  1. `$ sudo mysql` and then in the mysql shell:
    1. `CREATE DATABASE pong;`
    1. `exit`
  1. `$ pip install mysql-python`
    1. Do NOT use mysql-connector.
    1. This step might fail on Windows. If it does, download a wheel and install that.
  1. Update database tables `$ alembic upgrade head` (needs project on python system path)

1. If starting from absolute scratch you need to configure alembic
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

  1. To set up the database url, make a file called `config.py` which looks like this:

    ```
    config = {
        'DB_URL': <database url>
    } 
    ```

1. To make a new migration do `$ alembic revision --autogenerate -m "<message>"`
