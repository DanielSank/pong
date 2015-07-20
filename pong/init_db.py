import sqlalchemy as sa
import sqlalchemy.orm as orm
import assemblies.config as C


import assemblies.models as models


def initialize(db_url):
    engine = sa.create_engine(db_url, echo=True)
    Session = orm.sessionmaker(bind=engine)
    session = Session()
    session.add_all([
        models.User(name='foo'),
        models.User(name='bar'),
    ])
    session.commit()


def main():
    initialize(C.config['DB_URL'])


if __name__ == "__main__":
    main()
